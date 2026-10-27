import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import fetch_popular_papers as papers


def make_paper(arxiv_id: str, title: str, citations: int = 1000) -> dict:
    return {
        "paperId": arxiv_id,
        "title": title,
        "authors": [{"name": "Test Author"}],
        "year": 2017,
        "citationCount": citations,
        "venue": "Test Venue",
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "externalIds": {"ArXiv": arxiv_id},
        "fieldsOfStudy": ["Computer Science"],
    }


class PopularPapersTests(unittest.TestCase):
    def setUp(self) -> None:
        self.foundations = [
            make_paper(identifier.removeprefix("ARXIV:"), title)
            for identifier, title in zip(
                papers.FOUNDATION_IDS,
                ["Attention Is All You Need", "BERT", "T5", "GPT-3", "InstructGPT", "LLaMA", "Llama 2"],
            )
        ]
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "papers.md"
        self.original = make_paper("2005.11401", "RAG", 500)
        self.output.write_text("# Papers\n", encoding="utf-8")
        papers.save_to_markdown("RAG", [self.original], str(self.output))

    def test_refresh_adds_attention_and_is_idempotent(self) -> None:
        fetcher = Mock()
        live = {papers.paper_lookup_id(p): p for p in [*self.foundations, self.original]}
        fetcher.batch_papers.side_effect = lambda ids, fields=None: [
            live[identifier] if fields is None else {
                "paperId": live[identifier]["paperId"],
                "citationCount": live[identifier]["citationCount"],
            } for identifier in ids
        ]
        for _ in range(2):
            papers.refresh_existing_markdown(fetcher, str(self.output), 100, 50)
            sections = papers.parse_existing_markdown(str(self.output))
            self.assertEqual(sections[0][0], papers.FOUNDATION_TOPIC)
            titles = [p["title"] for _, entries in sections for p in entries]
            self.assertEqual(titles.count("Attention Is All You Need"), 1)
            self.assertEqual(titles.count("RAG"), 1)
            self.assertEqual(len(titles), 8)

    def test_missing_foundation_leaves_output_unchanged(self) -> None:
        fetcher = Mock()
        fetcher.batch_papers.return_value = [None] * len(papers.FOUNDATION_IDS)
        before = self.output.read_bytes()
        with self.assertRaisesRegex(RuntimeError, "foundational"):
            papers.refresh_existing_markdown(fetcher, str(self.output), 100, 50)
        self.assertEqual(self.output.read_bytes(), before)

    def test_foundations_respect_filters_and_citation_order(self) -> None:
        fetcher = Mock()
        self.foundations[0]["citationCount"] = 10000
        self.foundations[1]["citationCount"] = 99
        self.foundations[2]["fieldsOfStudy"] = ["Biology"]
        fetcher.batch_papers.return_value = self.foundations
        result = papers.fetch_foundational_papers(fetcher, 100)
        self.assertEqual(result[0]["title"], "Attention Is All You Need")
        self.assertEqual(len(result), 5)

    def test_foundation_discovery_only_requests_metadata_for_unknown_papers(self) -> None:
        fetcher = Mock()
        fetcher.batch_papers.side_effect = [
            [self.foundations[-1]],
            [{"paperId": p["paperId"], "citationCount": 2000} for p in self.foundations[:-1]],
        ]
        result = papers.fetch_foundational_papers(fetcher, 100, self.foundations[:-1])
        self.assertEqual(fetcher.batch_papers.call_args_list[0].args, ([papers.FOUNDATION_IDS[-1]],))
        self.assertEqual(fetcher.batch_papers.call_args_list[1].args, (papers.FOUNDATION_IDS[:-1],))
        self.assertEqual(fetcher.batch_papers.call_args_list[1].kwargs, {"fields": ["citationCount"]})
        self.assertEqual(result[0]["title"], "Attention Is All You Need")
        self.assertEqual(result[0]["citationCount"], 2000)
        self.assertEqual(len(result), 7)

    def test_missing_existing_entry_is_preserved_and_reported(self) -> None:
        fetcher = Mock()
        fetcher.batch_papers.side_effect = [self.foundations, [None]]
        papers.refresh_existing_markdown(fetcher, str(self.output), 100, 50)
        text = self.output.read_text(encoding="utf-8")
        self.assertIn("### 1. RAG", text)
        self.assertIn("Warning: 1 existing entries could not be refreshed", text)

    def test_search_uses_server_citation_ranking(self) -> None:
        fetcher = papers.SemanticScholarFetcher(
            user_agent=None, api_key=None, timeout=1, max_retries=1,
            backoff=0, request_delay=0, jitter=0,
        )
        fetcher.session = Mock()
        fetcher.session.get.return_value.status_code = 200
        fetcher.session.get.return_value.json.return_value = {"data": self.foundations}
        self.assertEqual(len(fetcher.search_papers("transformer", limit=2)), 2)
        args, kwargs = fetcher.session.get.call_args
        self.assertTrue(args[0].endswith("/paper/search/bulk"))
        self.assertEqual(kwargs["params"]["sort"], "citationCount:desc")
        self.assertEqual(kwargs["params"]["fieldsOfStudy"], "Computer Science")

    def test_singleton_batch_uses_batch_endpoint(self) -> None:
        fetcher = papers.SemanticScholarFetcher(
            user_agent=None, api_key=None, timeout=1, max_retries=1,
            backoff=0, request_delay=0, jitter=0,
        )
        fetcher.session = Mock()
        fetcher.session.post.return_value.status_code = 200
        fetcher.session.post.return_value.json.return_value = [self.original]
        self.assertEqual(fetcher.batch_papers(["ARXIV:2005.11401"]), [self.original])
        fetcher.session.get.assert_not_called()

    def test_discovery_checks_all_queries_before_selecting_top_n(self) -> None:
        fetcher = Mock()
        fetcher.batch_papers.return_value = self.foundations
        fetcher.get_papers_sorted_by_citations.side_effect = [
            [make_paper(f"2001.{index:05}", f"Paper {index}", 1000 + index)]
            for index in range(8)
        ]
        with (
            patch.object(papers, "SemanticScholarFetcher", return_value=fetcher),
            patch.object(sys, "argv", ["fetch_popular_papers", "--output", str(self.output), "--top-n", "1"]),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            papers.main()
        sections = papers.parse_existing_markdown(str(self.output))
        self.assertEqual(fetcher.get_papers_sorted_by_citations.call_count, 8)
        self.assertEqual(sections[1][1][0]["title"], "Paper 3")
        self.assertEqual(sections[2][1][0]["title"], "Paper 7")
        self.assertEqual(sections[0][1][0]["title"], "Attention Is All You Need")

    def test_discovery_reports_failed_queries_in_output(self) -> None:
        fetcher = Mock()
        fetcher.batch_papers.return_value = self.foundations
        fetcher.get_papers_sorted_by_citations.side_effect = [
            RuntimeError("rate limited"),
            *[[self.original] for _ in range(7)],
        ]
        with (
            patch.object(papers, "SemanticScholarFetcher", return_value=fetcher),
            patch.object(sys, "argv", ["fetch_popular_papers", "--output", str(self.output)]),
            contextlib.redirect_stdout(io.StringIO()),
            self.assertRaisesRegex(RuntimeError, "Partial discovery saved"),
        ):
            papers.main()
        self.assertIn("Warning: 1 discovery queries failed", self.output.read_text(encoding="utf-8"))

    def test_existing_foundations_use_citation_only_refresh_and_preserve_abstracts(self) -> None:
        papers.save_to_markdown(papers.FOUNDATION_TOPIC, self.foundations, str(self.output))
        fetcher = Mock()
        fetcher.batch_papers.return_value = [
            {"paperId": "rag-id", "citationCount": 1000},
            {"paperId": "attention-id", "citationCount": 200000},
            *[{"paperId": p["paperId"], "citationCount": p["citationCount"]} for p in self.foundations[1:]],
        ]
        papers.refresh_existing_markdown(fetcher, str(self.output), 100, 20)
        fetcher.batch_papers.assert_called_once_with(
            ["ARXIV:2005.11401", *papers.FOUNDATION_IDS], fields=["citationCount"],
        )
        entries = [p for _, section in papers.parse_existing_markdown(str(self.output)) for p in section]
        self.assertEqual(entries[1]["title"], "Attention Is All You Need")
        self.assertEqual(entries[1]["citationCount"], 200000)
        self.assertEqual(entries[1]["externalIds"], {"ArXiv": "1706.03762"})

    def test_discovery_pauses_on_exhausted_rate_limit_without_replacing_output(self) -> None:
        fetcher = Mock()
        fetcher.batch_papers.return_value = self.foundations
        fetcher.get_papers_sorted_by_citations.side_effect = [
            [self.original], papers.RateLimitDeferred("HTTP 429"),
        ]
        before = self.output.read_bytes()
        with (
            patch.object(papers, "SemanticScholarFetcher", return_value=fetcher),
            patch.object(sys, "argv", ["fetch_popular_papers", "--output", str(self.output)]),
            contextlib.redirect_stdout(io.StringIO()),
            self.assertRaisesRegex(papers.RateLimitDeferred, "Discovery paused"),
        ):
            papers.main()
        self.assertEqual(fetcher.get_papers_sorted_by_citations.call_count, 2)
        self.assertEqual(self.output.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
