import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import update_citation_counts as updater
from utils.semantic_scholar import SemanticScholarSession


CONTENT = """# Best Practices

## **RAG Best Practices**

### **RAG Research (Ranked by cite count >=100)**

- [RAG paper📑](https://arxiv.org/abs/2403.10131): RAG description. (Citations: 500)
- [Clinical paper📑](https://www.semanticscholar.org/paper/965a0969b460f9246158d88fb28e21c5d80d0a8b): Clinical description. (Citations: 300)

---

## **Agent Best Practices**

### **Agent Research (Ranked by cite count >=100)**

- [Agent paper📑](https://arxiv.org/abs/2401.07312): Agent description. (Citations: 200)

### **Security and Governance**

Unrelated content.
"""


class CitationUpdateTests(unittest.TestCase):
    def test_refresh_updates_arxiv_and_semantic_links_and_sorts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "best_practices.md"
            path.write_text(CONTENT, encoding="utf-8")
            fetcher = Mock()
            fetcher.session = SemanticScholarSession(Path(directory) / "cache", request_delay=1, jitter=0)
            fetcher.batch_papers.return_value = [{"citationCount": 450}]
            cached = {
                "ARXIV:2403.10131": {"citationCount": 550},
                "965a0969b460f9246158d88fb28e21c5d80d0a8b": {"citationCount": 800},
            }
            with (
                patch.object(updater, "SemanticScholarFetcher", return_value=fetcher),
                patch.object(fetcher.session, "cached_papers", return_value=cached),
            ):
                updated = updater.update_ranked_sections(
                    path, timeout=1, max_retries=1, sleep_s=1, dry_run=False, sort_only=False,
                )
            text = path.read_text(encoding="utf-8")
        self.assertEqual(updated, 3)
        fetcher.batch_papers.assert_called_once_with(["ARXIV:2401.07312"], fields=["citationCount"])
        self.assertIn("Clinical description. (Citations: 800)", text)
        self.assertIn("RAG description. (Citations: 550)", text)
        self.assertIn("Agent description. (Citations: 450)", text)
        self.assertLess(text.index("Clinical paper"), text.index("RAG paper"))
        self.assertIn("### **Security and Governance**\n\nUnrelated content.", text)

    def test_partial_failure_preserves_missing_counts_and_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "best_practices.md"
            path.write_text(CONTENT, encoding="utf-8")
            fetcher = Mock()
            fetcher.session = SemanticScholarSession(Path(directory) / "cache", request_delay=1, jitter=0)
            fetcher.batch_papers.side_effect = updater.QueryFetchError("HTTP 429")
            with (
                patch.object(updater, "SemanticScholarFetcher", return_value=fetcher),
                patch.object(fetcher.session, "cached_papers", return_value={
                    "ARXIV:2403.10131": {"citationCount": 550},
                }),
                self.assertRaisesRegex(updater.QueryFetchError, "Partial citation refresh"),
            ):
                updater.update_ranked_sections(
                    path, timeout=1, max_retries=1, sleep_s=1, dry_run=False, sort_only=False,
                )
            text = path.read_text(encoding="utf-8")
        self.assertIn("RAG description. (Citations: 550)", text)
        self.assertIn("Clinical description. (Citations: 300)", text)
        self.assertIn("Agent description. (Citations: 200)", text)
        self.assertIn("2 unavailable. Previous counts are retained", text)

    def test_unrecognized_citation_link_fails_explicitly(self) -> None:
        content = CONTENT.replace("https://arxiv.org/abs/2403.10131", "https://example.com/paper")
        with self.assertRaisesRegex(ValueError, "unsupported or malformed links"):
            updater.extract_papers_from_ranked_section(content, "RAG Research (Ranked by cite count >=100)")

    def test_sort_only_makes_no_api_requests(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "best_practices.md"
            path.write_text(CONTENT, encoding="utf-8")
            with patch.object(updater, "SemanticScholarFetcher") as fetcher:
                updater.update_ranked_sections(
                    path, timeout=1, max_retries=1, sleep_s=1, dry_run=False, sort_only=True,
                )
            fetcher.assert_not_called()
            self.assertEqual(path.read_text(encoding="utf-8"), CONTENT)

    def test_adds_only_over_100_and_deduplicates_both_sections(self) -> None:
        content = CONTENT.replace(
            "### **RAG Research (Ranked",
            "### **RAG Research**\n\n"
            "- [One hundred📑](https://arxiv.org/abs/2501.00001): Below cutoff.\n"
            "- [Qualifying📑](https://arxiv.org/pdf/2501.00002): Useful paper.\n"
            "- [Alternate ID📑](https://arxiv.org/abs/2501.00003): Already ranked.\n"
            "- [RAG paper📑](https://arxiv.org/abs/2403.10131): Duplicate.\n\n"
            "### **RAG Research (Ranked",
        ).replace(
            "### **Agent Research (Ranked",
            "### **Tool Use**\n\n"
            "  > - [Nested paper📑](https://arxiv.org/html/2501.00004) [Jan 2025]\n\n"
            "### **Agent Research (Ranked",
        )
        cached = {
            "ARXIV:2403.10131": {"citationCount": 500},
            "965a0969b460f9246158d88fb28e21c5d80d0a8b": {"citationCount": 300},
            "ARXIV:2401.07312": {"citationCount": 200},
            "ARXIV:2501.00001": {"citationCount": 100},
            "ARXIV:2501.00002": {"citationCount": 101},
            "ARXIV:2501.00003": {
                "citationCount": 300, "paperId": "965a0969b460f9246158d88fb28e21c5d80d0a8b",
            },
            "ARXIV:2501.00004": {"citationCount": 250},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "best_practices.md"
            path.write_text(content, encoding="utf-8")
            fetcher = Mock()
            fetcher.session = SemanticScholarSession(Path(directory) / "cache", request_delay=1, jitter=0)
            with (
                patch.object(updater, "SemanticScholarFetcher", return_value=fetcher),
                patch.object(fetcher.session, "cached_papers", return_value=cached),
            ):
                updater.update_ranked_sections(
                    path, timeout=1, max_retries=1, sleep_s=1, dry_run=False, sort_only=False,
                )
                first_run = path.read_text(encoding="utf-8")
                updater.update_ranked_sections(
                    path, timeout=1, max_retries=1, sleep_s=1, dry_run=False, sort_only=False,
                )
            updated = path.read_text(encoding="utf-8")
        rag = updater.extract_papers_from_ranked_section(updated, "RAG Research (Ranked by cite count >=100)")
        agent = updater.extract_papers_from_ranked_section(updated, "Agent Research (Ranked by cite count >=100)")
        self.assertEqual({paper[1] for paper in rag}, {
            "ARXIV:2403.10131", "965a0969b460f9246158d88fb28e21c5d80d0a8b", "ARXIV:2501.00002",
        })
        self.assertEqual({paper[1] for paper in agent}, {"ARXIV:2401.07312", "ARXIV:2501.00004"})
        self.assertEqual([paper[2] for paper in agent], [250, 200])
        self.assertEqual(updated, first_run)
        self.assertLess(updated.index("Qualifying📑", updated.index("Ranked by cite count")), updated.index("\n---"))
        fetcher.batch_papers.assert_not_called()


if __name__ == "__main__":
    unittest.main()
