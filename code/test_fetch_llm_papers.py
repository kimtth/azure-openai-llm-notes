import tempfile
import unittest
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import Mock, patch

import fetch_llm_papers as papers
import fetch_popular_papers as popular


class CitationRefreshTests(unittest.TestCase):
    def test_topic_discovery_can_keep_more_than_50_eligible_papers(self) -> None:
        fetcher = papers.SemanticScholarFetcher(
            user_agent=None, api_key=None, timeout=1, max_retries=1,
            backoff=0, request_delay=1, jitter=0,
        )
        results = [
            {
                "paperId": f"paper-{i}", "title": f"Language model agent paper {i}",
                "fieldsOfStudy": ["Computer Science"], "citationCount": 1000 - i,
            }
            for i in range(65)
        ]
        with patch.object(fetcher, "search_papers", return_value=results):
            found = fetcher.fetch_topic("LLM Agents", ["language model agent"], 0, 150, {})
            limited = fetcher.fetch_topic("LLM Agents", ["language model agent"], 50, 150, {})
        self.assertEqual(len(found), 65)
        self.assertEqual(len(limited), 50)
        self.assertEqual([p["citationCount"] for p in found], sorted(
            [p["citationCount"] for p in found], reverse=True,
        ))

    def test_citation_ranked_search_requests_bulk_sort(self) -> None:
        fetcher = papers.SemanticScholarFetcher(
            user_agent=None, api_key=None, timeout=1, max_retries=1,
            backoff=0, request_delay=1, jitter=0,
        )
        fetcher.session = Mock()
        fetcher.session.get.return_value.status_code = 200
        fetcher.session.get.return_value.json.return_value = {"data": [
            {"paperId": "first"}, {"paperId": "second"},
        ]}
        result = fetcher.search_papers('"language model"', limit=1, citation_ranked=True)
        self.assertEqual(result, [{"paperId": "first"}])
        args, kwargs = fetcher.session.get.call_args
        self.assertTrue(args[0].endswith("/paper/search/bulk"))
        self.assertEqual(kwargs["params"]["sort"], "citationCount:desc")
        self.assertEqual(kwargs["params"]["fieldsOfStudy"], "Computer Science")

    def test_merge_popular_sources_and_citation_search_without_replacing_existing(self) -> None:
        original = {
            "paperId": "old", "title": "Original language model", "citationCount": 200,
            "externalIds": {"ArXiv": "2309.07864"}, "topics": ["LLM Agents"],
        }
        bert = {
            "paperId": "bert-id", "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            "citationCount": 123375, "authors": [{"name": "Author"}], "year": 2018,
            "fieldsOfStudy": ["Computer Science"], "externalIds": {"ArXiv": "1810.04805"},
            "url": "https://www.semanticscholar.org/paper/bert-id",
        }
        new_agent = {
            "paperId": "new-agent", "title": "Language model agents",
            "citationCount": 500, "fieldsOfStudy": ["Computer Science"],
            "externalIds": {"ArXiv": "2308.11432"},
        }
        duplicate_title = {
            **new_agent, "paperId": "another-id", "title": original["title"].upper(),
            "externalIds": {"ArXiv": "2307.11111"},
        }
        unrelated = {
            **new_agent, "paperId": "bio", "title": "Language model agents in biology",
            "fieldsOfStudy": ["Biology"], "externalIds": {"ArXiv": "2307.22222"},
        }
        fetcher = Mock()
        fetcher.search_papers.return_value = [new_agent, duplicate_title, unrelated]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "landscape.md"
            source = Path(directory) / "popular.md"
            papers._flush_output(str(output), [original], 150, refresh_note="Citation data refreshed for 1 existing entries.")
            source.write_text("# Popular papers\n", encoding="utf-8")
            popular.save_to_markdown("Foundational LLMs & Transformers", [bert], str(source))
            with patch.dict(papers.POPULAR_DISCOVERY_QUERIES, {"LLM Agents": ['"language agent"']}, clear=True):
                papers.discover_popular_papers(fetcher, str(output), str(source), 150)
            result = papers._load_existing_markdown(str(output))
            text = output.read_text(encoding="utf-8")
        self.assertEqual({p["title"] for p in result}, {original["title"], bert["title"], new_agent["title"]})
        self.assertIn("Citation data refreshed for 1 existing entries.", text)
        self.assertIn("Popular-paper discovery complete; 1/1", text)
        fetcher.search_papers.assert_called_once_with('"language agent"', limit=1000, citation_ranked=True)

    def test_bulk_discovery_requires_language_focus_not_vision_or_gan_background(self) -> None:
        cases = [
            ("An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale",
             "The Transformer is the standard for natural language processing. We apply it to image classification.", False),
            ("Swin Transformer: Hierarchical Vision Transformer using Shifted Windows",
             "We adapt Transformers from language to vision.", False),
            ("Improved Training of Wasserstein GANs",
             "We train generative adversarial networks. We also try language models over discrete data.", False),
            ("Autoformer: Transformers for Time-Series Forecasting",
             "Transformers are successful in natural language processing.", False),
            ("BERT: Pre-training for Language Understanding", "", True),
            ("Training Verifiers to Solve Math Word Problems",
             "We train language models to solve math word problems.", True),
            ("Longformer: The Long-Document Transformer",
             "We evaluate the model on character-level language modeling.", True),
            ("Reformer: The Efficient Transformer",
             "We improve the memory efficiency of Transformers on long sequences.", True),
            ("Attention with Linear Biases Enables Input Length Extrapolation",
             "We introduce a position method for transformer models.", True),
            ("Vision-and-Language Tasks", "A model of images and text.", True),
            ("Unspecified Transformer", "", False),
        ]
        for title, abstract, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(papers._is_language_discovery({"title": title, "abstract": abstract}), expected)

    def test_bulk_discovery_merges_all_returned_results_and_filters_false_positives(self) -> None:
        original = {"paperId": "old", "title": "Original language model", "citationCount": 200,
                    "externalIds": {"ArXiv": "2309.07864"}, "topics": ["LLM Agents"]}
        bert = {"title": "BERT: Language Understanding", "citationCount": 500, "authors": [],
                "year": 2018, "fieldsOfStudy": ["Computer Science"],
                "externalIds": {"ArXiv": "1810.04805"}, "url": "https://arxiv.org/abs/1810.04805"}
        candidates = [
            {"paperId": f"agent-{i}", "title": f"Language model agent paper {i}",
             "citationCount": 500, "fieldsOfStudy": ["Computer Science"]}
            for i in range(101)
        ]
        candidates.append({"paperId": "vision", "title": "Vision Transformer for Image Recognition",
                           "abstract": "Transformers are used for natural language processing.",
                           "citationCount": 500, "fieldsOfStudy": ["Computer Science"]})
        fetcher = Mock()
        fetcher.search_papers.return_value = candidates
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "landscape.md"
            source = Path(directory) / "popular.md"
            papers._flush_output(str(output), [original], 150)
            source.write_text("# Popular papers\n", encoding="utf-8")
            popular.save_to_markdown("Foundational LLMs & Transformers", [bert], str(source))
            with patch.dict(papers.POPULAR_DISCOVERY_QUERIES, {"LLM Agents": ["query"]}, clear=True):
                papers.discover_popular_papers(fetcher, str(output), str(source), 150)
            result = papers._load_existing_markdown(str(output))
        titles = {paper["title"] for paper in result}
        self.assertIn("Language model agent paper 100", titles)
        self.assertNotIn("Vision Transformer for Image Recognition", titles)

    def test_discovery_failure_saves_imports_and_successful_queries_for_resume(self) -> None:
        original = {
            "paperId": "old", "title": "Original language model", "citationCount": 200,
            "externalIds": {"ArXiv": "2309.07864"}, "topics": ["LLM Agents"],
        }
        agent = {
            "paperId": "agent", "title": "Language model agents", "citationCount": 500,
            "fieldsOfStudy": ["Computer Science"], "externalIds": {"ArXiv": "2308.11432"},
        }
        bert = {
            "title": "BERT: Transformers", "citationCount": 500, "authors": [], "year": 2018,
            "fieldsOfStudy": ["Computer Science"], "externalIds": {"ArXiv": "1810.04805"},
            "url": "https://arxiv.org/abs/1810.04805",
        }
        fetcher = Mock()
        fetcher.search_papers.side_effect = [[agent], papers.QueryFetchError("HTTP 429")]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "landscape.md"
            source = Path(directory) / "popular.md"
            papers._flush_output(str(output), [original], 150, refresh_note="Citation data refreshed for 1 existing entries.")
            source.write_text("# Popular papers\n", encoding="utf-8")
            popular.save_to_markdown("Foundational LLMs & Transformers", [bert], str(source))
            with (
                patch.dict(papers.POPULAR_DISCOVERY_QUERIES, {"LLM Agents": ["first", "second"]}, clear=True),
                self.assertRaisesRegex(papers.QueryFetchError, "1/2 queries completed"),
            ):
                papers.discover_popular_papers(fetcher, str(output), str(source), 150)
            result = papers._load_existing_markdown(str(output))
            text = output.read_text(encoding="utf-8")
        self.assertEqual(len(result), 3)
        self.assertIn("Popular-paper discovery incomplete; 1/2", text)
        self.assertIn("Citation data refreshed for 1 existing entries.", text)

    def test_architecture_discovery_includes_foundation_when_search_misses(self) -> None:
        foundation = {
            "paperId": "204e3073870fae3d05bcbc2f6a8e263d9b72e776",
            "title": "Attention is All you Need",
            "citationCount": 198575,
            "abstract": "We propose the Transformer, based solely on attention mechanisms.",
            "fieldsOfStudy": ["Computer Science"],
            "externalIds": {"ArXiv": "1706.03762"},
        }
        fetcher = Mock()
        fetcher.batch_papers.return_value = [foundation]
        fetcher.fetch_topic.return_value = []
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "papers.md"
            with (
                patch.object(papers, "SemanticScholarFetcher", return_value=fetcher),
                patch.object(sys, "argv", [
                    "fetch_llm_papers", "--output", str(output),
                    "--topics", "LLM Architecture Innovations",
                ]),
            ):
                papers.main()
            result = papers._load_existing_markdown(str(output))
        self.assertEqual(len(result), 1)
        self.assertEqual(papers._paper_lookup_id(result[0]), "ARXIV:1706.03762")
        self.assertIn("LLM Architecture Innovations", result[0]["topics"])
        fetcher.batch_papers.assert_called_once_with(["ARXIV:1706.03762"])
        self.assertIn("attention is all you need", papers.TOPICS["LLM Architecture Innovations"])

    def test_foundation_is_deduplicated_against_other_search_paper_id(self) -> None:
        foundation = {
            "paperId": "canonical", "title": "Attention is All you Need", "citationCount": 198575,
            "abstract": "The Transformer relies on attention.", "fieldsOfStudy": ["Computer Science"],
            "externalIds": {"ArXiv": "1706.03762"},
        }
        fetcher = Mock()
        fetcher.batch_papers.return_value = [foundation]
        fetcher.fetch_topic.return_value = [{**foundation, "paperId": "alternate"}]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "papers.md"
            with (
                patch.object(papers, "SemanticScholarFetcher", return_value=fetcher),
                patch.object(sys, "argv", [
                    "fetch_llm_papers", "--output", str(output), "--topics", "LLM Architecture Innovations",
                ]),
            ):
                papers.main()
            result = papers._load_existing_markdown(str(output))
        self.assertEqual(len(result), 1)
        self.assertEqual(papers._paper_lookup_id(result[0]), "ARXIV:1706.03762")

    def test_missing_foundation_leaves_existing_output_unchanged(self) -> None:
        fetcher = Mock()
        fetcher.batch_papers.return_value = [None]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "papers.md"
            output.write_text("unchanged", encoding="utf-8")
            with (
                patch.object(papers, "SemanticScholarFetcher", return_value=fetcher),
                patch.object(sys, "argv", [
                    "fetch_llm_papers", "--output", str(output), "--topics", "LLM Architecture Innovations",
                ]),
                self.assertRaisesRegex(papers.QueryFetchError, "foundational architecture"),
            ):
                papers.main()
            self.assertEqual(output.read_text(encoding="utf-8"), "unchanged")
        fetcher.fetch_topic.assert_not_called()

    def test_foundation_obeys_citation_threshold_and_topic_scope(self) -> None:
        foundation = {
            "paperId": "canonical", "title": "Attention is All you Need", "citationCount": 100,
            "fieldsOfStudy": ["Computer Science"], "externalIds": {"ArXiv": "1706.03762"},
        }
        fetcher = Mock()
        fetcher.batch_papers.return_value = [foundation]
        fetcher.fetch_topic.return_value = []
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "papers.md"
            with (
                patch.object(papers, "SemanticScholarFetcher", return_value=fetcher),
                patch.object(sys, "argv", [
                    "fetch_llm_papers", "--output", str(output), "--topics", "LLM Architecture Innovations",
                ]),
            ):
                papers.main()
            self.assertEqual(papers._load_existing_markdown(str(output)), [])
            fetcher.reset_mock()
            with (
                patch.object(papers, "SemanticScholarFetcher", return_value=fetcher),
                patch.object(sys, "argv", ["fetch_llm_papers", "--output", str(output), "--topics", "GUI Agents"]),
            ):
                papers.main()
            fetcher.batch_papers.assert_not_called()

    def test_completed_architecture_checkpoint_still_adds_missing_foundation(self) -> None:
        foundation = {
            "paperId": "canonical", "title": "Attention is All you Need", "citationCount": 198575,
            "fieldsOfStudy": ["Computer Science"], "externalIds": {"ArXiv": "1706.03762"},
        }
        fetcher = Mock()
        fetcher.batch_papers.return_value = [foundation]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "papers.md"
            checkpoint = output.with_suffix(".checkpoint.json")
            papers._save_checkpoint(str(checkpoint), [], ["LLM Architecture Innovations"], {}, [])
            with (
                patch.object(papers, "SemanticScholarFetcher", return_value=fetcher),
                patch.object(sys, "argv", [
                    "fetch_llm_papers", "--output", str(output), "--topics", "LLM Architecture Innovations",
                ]),
            ):
                papers.main()
            result = papers._load_existing_markdown(str(output))
        self.assertEqual(len(result), 1)
        self.assertEqual(papers._paper_lookup_id(result[0]), "ARXIV:1706.03762")
        fetcher.fetch_topic.assert_not_called()

    def test_foundation_requires_computer_science_and_matching_arxiv_id(self) -> None:
        foundation = {
            "paperId": "canonical", "title": "Attention is All you Need", "citationCount": 198575,
            "fieldsOfStudy": ["Computer Science"], "externalIds": {"ArXiv": "1706.03762"},
        }
        for invalid in (
            {**foundation, "fieldsOfStudy": ["Biology"]},
            {**foundation, "externalIds": {"ArXiv": "1706.03763"}},
            {**foundation, "citationCount": None},
        ):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as directory:
                fetcher = Mock()
                fetcher.batch_papers.return_value = [invalid]
                output = Path(directory) / "papers.md"
                output.write_text("unchanged", encoding="utf-8")
                with (
                    patch.object(papers, "SemanticScholarFetcher", return_value=fetcher),
                    patch.object(sys, "argv", [
                        "fetch_llm_papers", "--output", str(output), "--topics", "LLM Architecture Innovations",
                    ]),
                    self.assertRaises(papers.QueryFetchError),
                ):
                    papers.main()
                self.assertEqual(output.read_text(encoding="utf-8"), "unchanged")

    def test_checkpoints_only_resume_within_the_same_utc_month(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "checkpoint.json"
            papers._save_checkpoint(str(checkpoint), [], ["LLM Agents"], {"query": []}, [])
            self.assertEqual(papers._load_checkpoint(str(checkpoint))[2], ["LLM Agents"])
            data = json.loads(checkpoint.read_text(encoding="utf-8"))
            self.assertEqual(data["period"], datetime.now(UTC).strftime("%Y-%m"))
            data["period"] = "2000-01"
            checkpoint.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(papers._load_checkpoint(str(checkpoint)), ([], set(), [], {}, []))

    def test_lightweight_refresh_preserves_metadata_and_missing_entries(self) -> None:
        original = {
            "paperId": "old-id", "title": "Original title", "citationCount": 200,
            "abstract": "Original description", "topics": ["LLM Agents"],
            "externalIds": {"ArXiv": "2309.07864"},
        }
        missing = {**original, "paperId": "missing", "externalIds": {"ArXiv": "2308.11432"}}
        fetcher = Mock()
        fetcher.batch_papers.return_value = [{"paperId": "live-id", "citationCount": 300}, None]
        with (
            patch.object(papers, "_load_existing_markdown", return_value=[original, missing]),
            patch.object(papers, "_flush_output") as flush,
        ):
            papers.refresh_existing_papers(fetcher, "unused.md", 150, 20)
        fetcher.batch_papers.assert_called_once_with(
            ["ARXIV:2309.07864", "ARXIV:2308.11432"], fields=["citationCount"],
        )
        refreshed = flush.call_args.args[1]
        self.assertEqual(refreshed[0], {**original, "paperId": "live-id", "citationCount": 300})
        self.assertEqual(refreshed[1], missing)
        self.assertEqual(original["citationCount"], 200)
        self.assertIn("1 unavailable entries", flush.call_args.kwargs["refresh_note"])

    def test_refresh_preserves_discovery_note(self) -> None:
        original = {
            "title": "Original language model", "citationCount": 200,
            "externalIds": {"ArXiv": "2309.07864"}, "topics": ["LLM Agents"],
        }
        fetcher = Mock()
        fetcher.batch_papers.return_value = [{"citationCount": 300}]
        note = "Popular-paper discovery complete; 8/8 citation-ranked queries completed."
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "papers.md"
            papers._flush_output(str(output), [original], 150, discovery_note=note)
            papers.refresh_existing_papers(fetcher, str(output), 150, 20)
            text = output.read_text(encoding="utf-8")
        self.assertIn(note, text)
        self.assertIn("Citation data refreshed for 1 existing entries.", text)

    def test_partial_refresh_saves_successes_and_reports_failure(self) -> None:
        originals = [
            {"title": f"Paper {i}", "citationCount": 200, "externalIds": {"ArXiv": f"2309.{i:05}"}}
            for i in range(2)
        ]
        fetcher = Mock()
        fetcher.batch_papers.side_effect = [
            [{"paperId": "live-id", "citationCount": 300}],
            papers.QueryFetchError("rate limited"),
        ]
        with (
            patch.object(papers, "_load_existing_markdown", return_value=originals),
            patch.object(papers, "_flush_output") as flush,
            self.assertRaisesRegex(papers.QueryFetchError, "Partial citation refresh saved"),
        ):
            papers.refresh_existing_papers(fetcher, "unused.md", 150, 1)
        refreshed = flush.call_args.args[1]
        self.assertEqual(refreshed[0]["citationCount"], 300)
        self.assertEqual(refreshed[1]["citationCount"], 200)
        self.assertIn("1 unavailable entries", flush.call_args.kwargs["refresh_note"])

    def test_refresh_applies_cached_records_after_a_failed_pending_batch(self) -> None:
        originals = [
            {"title": f"Paper {i}", "citationCount": 200, "externalIds": {"ArXiv": f"2309.{i:05}"}}
            for i in range(3)
        ]
        with tempfile.TemporaryDirectory() as directory:
            fetcher = Mock()
            fetcher.session = papers.SemanticScholarSession(Path(directory), request_delay=1, jitter=0)
            self.addCleanup(fetcher.session.close)
            fetcher.batch_papers.side_effect = papers.QueryFetchError("rate limited")
            with (
                patch.object(fetcher.session, "cached_papers", return_value={
                    "ARXIV:2309.00000": {"citationCount": 300},
                    "ARXIV:2309.00002": {"citationCount": 400},
                }),
                patch.object(papers, "_load_existing_markdown", return_value=originals),
                patch.object(papers, "_flush_output") as flush,
                self.assertRaisesRegex(papers.QueryFetchError, "Partial citation refresh saved"),
            ):
                papers.refresh_existing_papers(fetcher, "unused.md", 150, 20)
        fetcher.batch_papers.assert_called_once_with(["ARXIV:2309.00001"], fields=["citationCount"])
        self.assertEqual([p["citationCount"] for p in flush.call_args.args[1]], [300, 200, 400])
        self.assertIn("1 unavailable entries", flush.call_args.kwargs["refresh_note"])

    def test_failed_batch_does_not_overwrite_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "papers.md"
            output.write_text("unchanged", encoding="utf-8")
            fetcher = Mock()
            fetcher.batch_papers.side_effect = papers.QueryFetchError("rate limited")
            with (
                patch.object(papers, "_load_existing_markdown", return_value=[
                    {"externalIds": {"ArXiv": "2309.07864"}},
                ]),
                self.assertRaises(papers.QueryFetchError),
            ):
                papers.refresh_existing_papers(fetcher, str(output), 150, 20)
            self.assertEqual(output.read_text(encoding="utf-8"), "unchanged")


if __name__ == "__main__":
    unittest.main()
