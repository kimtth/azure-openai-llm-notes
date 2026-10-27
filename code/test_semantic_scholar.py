import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from email.utils import formatdate
from pathlib import Path
from threading import Event
from unittest.mock import patch

import requests

from utils.semantic_scholar import SemanticScholarSession


BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"


def response(payload, status=200, retry_after=None):
    result = requests.Response()
    result.status_code = status
    result._content = json.dumps(payload).encode("utf-8")
    if retry_after:
        result.headers["Retry-After"] = retry_after
    return result


class MonthlySessionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.cache_dir = Path(self.directory.name)
        self.now = 1800000000.0
        self.sleep_calls = []
        clock = patch("utils.semantic_scholar.time.time", side_effect=lambda: self.now)
        sleeper = patch("utils.semantic_scholar.time.sleep", side_effect=self.sleep)
        transport = patch.object(requests.Session, "request")
        self.addCleanup(clock.stop)
        self.addCleanup(sleeper.stop)
        self.addCleanup(transport.stop)
        clock.start()
        sleeper.start()
        self.transport = transport.start()
        self.session = self.new_session()

    def new_session(self):
        session = SemanticScholarSession(self.cache_dir, request_delay=5, jitter=0)
        self.addCleanup(session.close)
        return session

    def sleep(self, seconds):
        self.sleep_calls.append(seconds)
        self.now += seconds

    def batch(self, identifiers, session=None, fields="citationCount"):
        return (session or self.session).post(
            BATCH_URL, params={"fields": fields}, json={"ids": identifiers}, timeout=1,
        )

    def test_batch_cache_survives_restart_reordering_and_changed_batch_size(self) -> None:
        self.transport.side_effect = [
            response([{"paperId": "a", "citationCount": 1}, {"paperId": "b", "citationCount": 2}]),
            response([{"paperId": "c", "citationCount": 3}]),
        ]
        self.batch(["ARXIV:a", "ARXIV:b"])
        restarted = self.new_session()
        result = self.batch(["ARXIV:b", "ARXIV:c", "ARXIV:a"], restarted).json()
        self.assertEqual([p["citationCount"] for p in result], [2, 3, 1])
        self.assertEqual(self.transport.call_args.kwargs["json"]["ids"], ["ARXIV:c"])
        self.assertEqual(self.sleep_calls, [5])
        self.batch(["ARXIV:a"], restarted)
        self.assertEqual(self.transport.call_count, 2)
        self.assertEqual(self.sleep_calls, [5])

    def test_cached_papers_reads_only_successful_requested_ids_without_network(self) -> None:
        self.transport.return_value = response([{"paperId": "a", "citationCount": 1}, None])
        self.batch(["ARXIV:a", "ARXIV:b"])
        cached = self.session.cached_papers(["ARXIV:b", "ARXIV:a", "missing"], ["citationCount"])
        self.assertEqual(cached["ARXIV:a"]["citationCount"], 1)
        self.assertEqual(set(cached), {"ARXIV:a"})
        self.assertEqual(self.transport.call_count, 1)

    def test_null_records_are_retried_without_refetching_successes(self) -> None:
        self.transport.side_effect = [
            response([{"paperId": "a", "citationCount": 0}, None]),
            response([{"paperId": "b", "citationCount": 2}]),
        ]
        self.batch(["a", "b"])
        result = self.batch(["a", "b"]).json()
        self.assertEqual(result[0]["citationCount"], 0)
        self.assertEqual(self.transport.call_args.kwargs["json"]["ids"], ["b"])

    def test_http_errors_are_not_cached(self) -> None:
        self.transport.side_effect = [
            response({"message": "unavailable"}, 503),
            response([{"paperId": "a", "citationCount": 1}]),
        ]
        self.assertEqual(self.batch(["a"]).status_code, 503)
        self.assertEqual(self.batch(["a"]).status_code, 200)
        self.assertEqual(self.transport.call_count, 2)

    def test_cooldown_shared_between_sessions_and_grows_after_repeated_429(self) -> None:
        self.transport.side_effect = [
            response({}, 429), response({}, 429), response([{"paperId": "a", "citationCount": 1}]),
        ]
        self.batch(["a"])
        second = self.new_session()
        self.batch(["a"], second)
        self.batch(["a"])
        self.assertEqual(self.sleep_calls, [120, 240])
        with closing(sqlite3.connect(self.session.database)) as connection:
            failures = connection.execute("SELECT failures FROM pacing").fetchone()[0]
        self.assertEqual(failures, 0)

    def test_retry_after_seconds_and_http_date_are_respected(self) -> None:
        self.transport.side_effect = [
            response({}, 429, "1000"),
            response({}, 429, formatdate(self.now + 1500, usegmt=True)),
            response([{"paperId": "a", "citationCount": 1}]),
        ]
        self.batch(["a"])
        self.batch(["a"])
        self.batch(["a"])
        self.assertEqual(self.sleep_calls, [1000, 500])

    def test_invalid_retry_after_still_uses_conservative_cooldown(self) -> None:
        self.transport.side_effect = [
            response({}, 429, "invalid"), response([{"paperId": "a", "citationCount": 1}]),
        ]
        self.batch(["a"])
        self.batch(["a"])
        self.assertEqual(self.sleep_calls, [120])

    def test_month_rollover_expires_responses(self) -> None:
        self.transport.return_value = response([{"paperId": "a", "citationCount": 1}])
        with patch("utils.semantic_scholar.datetime") as clock:
            clock.now.return_value = datetime(2026, 10, 31, tzinfo=UTC)
            self.batch(["a"])
            clock.now.return_value = datetime(2026, 11, 1, tzinfo=UTC)
            self.batch(["a"])
        self.assertEqual(self.transport.call_count, 2)

    def test_search_caches_empty_results_and_seeds_citation_aliases(self) -> None:
        self.transport.side_effect = [
            response({"data": [{
                "paperId": "a", "externalIds": {"ArXiv": "1706.03762"},
                "citationCount": 10, "title": "Attention",
            }]}),
            response({"data": []}),
        ]
        params = {"query": "attention", "fields": "title,paperId,citationCount,externalIds"}
        self.session.get(SEARCH_URL, params=params)
        self.session.get(SEARCH_URL, params={**params, "fields": "externalIds,citationCount,paperId,title"})
        self.assertEqual(self.batch(["ARXIV:1706.03762"]).json()[0]["citationCount"], 10)
        empty_params = {**params, "query": "no matches"}
        self.session.get(SEARCH_URL, params=empty_params)
        self.session.get(SEARCH_URL, params=empty_params)
        self.assertEqual(self.transport.call_count, 2)

    def test_cache_keys_distinguish_fields_and_search_options(self) -> None:
        self.transport.side_effect = [
            response([{"paperId": "a", "citationCount": 10}]),
            response([{"paperId": "a", "title": "Title"}]),
            response({"data": []}),
            response({"data": []}),
        ]
        self.batch(["a"])
        self.batch(["a"], fields="title")
        self.session.get(SEARCH_URL, params={"query": "test", "fields": "title", "sort": "citationCount:desc"})
        self.session.get(SEARCH_URL, params={"query": "test", "fields": "title", "sort": "publicationDate:desc"})
        self.assertEqual(self.transport.call_count, 4)

    def test_single_paper_lookup_is_cached_and_seeds_batch_counts(self) -> None:
        self.transport.return_value = response({"paperId": "a", "citationCount": 10})
        url = BATCH_URL.removesuffix("/batch") + "/a"
        self.session.get(url, params={"fields": "citationCount"})
        self.session.get(url, params={"fields": "citationCount"})
        self.assertEqual(self.batch(["a"]).json(), [{"paperId": "a", "citationCount": 10}])
        self.assertEqual(self.transport.call_count, 1)

    def test_malformed_batch_does_not_cache_success_shaped_results(self) -> None:
        for payload in [[], [{}], [{"paperId": "a", "citationCount": None}], ["invalid"]]:
            with self.subTest(payload=payload):
                self.transport.return_value = response(payload)
                with self.assertRaises(ValueError):
                    self.batch(["a"])
        self.transport.return_value = response([{"paperId": "a", "citationCount": 1}])
        self.batch(["a"])
        self.assertEqual(self.transport.call_count, 5)

    def test_network_error_preserves_shared_pacing_and_releases_lock(self) -> None:
        self.transport.side_effect = [
            requests.ConnectionError("offline"), response([{"paperId": "a", "citationCount": 1}]),
        ]
        with self.assertRaises(requests.ConnectionError):
            self.batch(["a"])
        self.batch(["a"], self.new_session())
        self.assertEqual(self.sleep_calls, [5])

    def test_request_body_is_not_mutated(self) -> None:
        self.transport.return_value = response([{"paperId": "a", "citationCount": 1}])
        body = {"ids": ["a"]}
        self.session.post(BATCH_URL, params={"fields": "citationCount"}, json=body)
        self.assertEqual(body, {"ids": ["a"]})

    def test_concurrent_sessions_serialize_and_share_successes(self) -> None:
        second = self.new_session()
        entered = Event()
        release = Event()
        second_started = Event()

        def network(*args, **kwargs):
            entered.set()
            if not release.wait(5):
                raise TimeoutError("Test did not release first request")
            return response([{"paperId": "a", "citationCount": 1}])

        def second_request():
            second_started.set()
            return self.batch(["a"], second)

        self.transport.side_effect = network
        with ThreadPoolExecutor(max_workers=2) as executor:
            first = executor.submit(self.batch, ["a"])
            try:
                self.assertTrue(entered.wait(5))
                other = executor.submit(second_request)
                self.assertTrue(second_started.wait(5))
                self.assertFalse(other.done())
            finally:
                release.set()
            self.assertEqual(first.result(timeout=5).json(), other.result(timeout=5).json())
        self.assertEqual(self.transport.call_count, 1)

    def test_both_paper_fetchers_reuse_the_same_citation_cache(self) -> None:
        from fetch_llm_papers import SemanticScholarFetcher as LandscapeFetcher
        from fetch_popular_papers import SemanticScholarFetcher as PopularFetcher

        settings = dict(
            user_agent=None, api_key=None, timeout=1, max_retries=1, backoff=0,
            request_delay=5, jitter=0, cache_dir=self.cache_dir,
        )
        popular = PopularFetcher(**settings)
        landscape = LandscapeFetcher(**settings)
        self.addCleanup(popular.session.close)
        self.addCleanup(landscape.session.close)
        self.transport.return_value = response([{"paperId": "a", "citationCount": 1}])
        first = popular.batch_papers(["ARXIV:a"], fields=["citationCount"])
        second = landscape.batch_papers(["ARXIV:a"], fields=["citationCount"])
        self.assertEqual(first, second)
        self.assertEqual(self.transport.call_count, 1)

    def test_interrupted_landscape_refresh_resumes_after_output_is_resorted(self) -> None:
        import fetch_llm_papers as papers

        output = self.cache_dir / "papers.md"
        originals = [
            {
                "paperId": identifier, "title": f"Paper {identifier}",
                "citationCount": count, "topics": ["LLM Agents"],
                "externalIds": {"ArXiv": arxiv_id},
                "authors": [{"name": "Author"}], "year": 2023,
                "abstract": "An LLM agent research paper.",
            }
            for identifier, arxiv_id, count in [("a", "2309.07864", 1000), ("b", "2308.11432", 300)]
        ]
        papers._flush_output(str(output), originals, 150)
        settings = dict(
            user_agent=None, api_key=None, timeout=1, max_retries=1, backoff=0,
            request_delay=5, jitter=0, cache_dir=self.cache_dir,
        )
        self.transport.side_effect = [
            response([{"paperId": "a", "citationCount": 200}]),
            response({}, 503),
            response([{"paperId": "b", "citationCount": 500}]),
        ]
        fetcher = papers.SemanticScholarFetcher(**settings)
        self.addCleanup(fetcher.session.close)
        with self.assertRaisesRegex(papers.QueryFetchError, "Partial citation refresh saved"):
            papers.refresh_existing_papers(fetcher, str(output), 150, 1)
        self.assertEqual([p["title"] for p in papers._load_existing_markdown(str(output))], ["Paper b", "Paper a"])
        restarted = papers.SemanticScholarFetcher(**settings)
        self.addCleanup(restarted.session.close)
        papers.refresh_existing_papers(restarted, str(output), 150, 1)
        updated = papers._load_existing_markdown(str(output))
        self.assertEqual([p["citationCount"] for p in updated], [500, 200])
        self.assertNotIn("unavailable entries", output.read_text(encoding="utf-8"))
        self.assertEqual(self.transport.call_count, 3)

    def test_discovery_resume_reuses_successful_queries_and_retries_throttled_query(self) -> None:
        from fetch_popular_papers import SemanticScholarFetcher
        from utils.semantic_scholar import RateLimitDeferred

        settings = dict(
            user_agent=None, api_key=None, timeout=1, max_retries=1, backoff=0,
            request_delay=5, jitter=0, cache_dir=self.cache_dir,
        )
        self.transport.side_effect = [
            response({"data": [{"paperId": "a", "citationCount": 100}]}),
            response({}, 429),
            response({"data": [{"paperId": "b", "citationCount": 200}]}),
        ]
        fetcher = SemanticScholarFetcher(**settings)
        self.addCleanup(fetcher.session.close)
        fetcher.search_papers("first query")
        with self.assertRaises(RateLimitDeferred):
            fetcher.search_papers("second query")
        restarted = SemanticScholarFetcher(**settings)
        self.addCleanup(restarted.session.close)
        self.assertEqual(restarted.search_papers("first query")[0]["paperId"], "a")
        self.assertEqual(restarted.search_papers("second query")[0]["paperId"], "b")
        self.assertEqual(self.transport.call_count, 3)
        self.assertEqual(self.sleep_calls, [5, 120])


if __name__ == "__main__":
    unittest.main()
