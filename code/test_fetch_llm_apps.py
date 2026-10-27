import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import fetch_llm_apps as apps


LEGEND = "*⏸️ = archived or no commits to the default branch since 2025-10-02 (checked 2026-10-02)*"


class InactivityMarkerTests(unittest.TestCase):
    def test_round_trip_preserves_only_existing_markers_and_dated_legend(self) -> None:
        content = (
            "# Popular LLM Applications\n\n"
            f"{LEGEND}<br>\n\n"
            "1. [Owner/Marked](https://github.com/Owner/Marked): LLM agent. [Jan 2024] (⭐ 2,000) ⏸️\n"
            "2. [Owner/Active](https://github.com/Owner/Active): LLM agent. [Jan 2024] (⭐ 1,500)\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "apps.md"
            path.write_text(content, encoding="utf-8")
            existing = apps.parse_markdown_entries(path)
            legend = apps.parse_inactivity_legend(path)
            self.assertEqual(len(existing), 2)
            self.assertTrue(existing[0]["inactivity_marker"])
            self.assertFalse(existing[1]["inactivity_marker"])
            refreshed = [
                {"full_name": "owner/marked", "url": "https://github.com/owner/marked", "stars": 2200},
                {"full_name": "owner/active", "url": "https://github.com/owner/active", "stars": 1600},
                {"full_name": "owner/new", "url": "https://github.com/owner/new", "stars": 1200},
            ]
            apps.preserve_inactivity_markers(refreshed, existing)
            apps.save_markdown(
                refreshed, path, min_stars=1000, topics=[], search_terms=[], inactivity_legend=legend,
            )
            text = path.read_text(encoding="utf-8")
            saved = apps.parse_markdown_entries(path)
        self.assertIn(LEGEND, text)
        self.assertIn("unmarked repositories, including newer entries, may not have been checked", text)
        self.assertEqual([repo["inactivity_marker"] for repo in saved], [True, False, False])
        self.assertEqual(text.count("⏸️"), 2)

    def test_cannot_write_marker_without_dated_legend(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "apps.md"
            path.write_text("unchanged", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "without their dated legend"):
                apps.save_markdown(
                    [{"full_name": "owner/repo", "inactivity_marker": True}],
                    path, min_stars=1000, topics=[], search_terms=[],
                )
            self.assertEqual(path.read_text(encoding="utf-8"), "unchanged")

    def test_normal_and_append_refresh_keep_existing_marker(self) -> None:
        content = (
            "# Popular LLM Applications\n\n"
            f"{LEGEND}\n\n"
            "1. [Owner/Marked](https://github.com/Owner/Marked): LLM agent. [Jan 2024] (⭐ 2,000) ⏸️\n"
            "2. [Owner/Active](https://github.com/Owner/Active): LLM agent. [Jan 2024] (⭐ 1,500)\n"
        )
        raw = {
            "name": "Marked", "full_name": "owner/marked", "html_url": "https://github.com/owner/marked",
            "description": "An LLM agent", "stargazers_count": 2200, "topics": ["llm"],
            "created_at": "2024-01-01", "archived": False,
        }
        for append in (False, True):
            with self.subTest(append=append), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "apps.md"
                path.write_text(content, encoding="utf-8")
                argv = [
                    "fetch_llm_apps", "--output", str(path), "--topics", "llm",
                    "--search-terms", "AI agent", "--sleep", "0", "--show", "0",
                ]
                if append:
                    argv.append("--append")
                with (
                    patch.object(apps.sys, "argv", argv),
                    patch.object(apps.sys, "stdout", Mock()),
                    patch.object(apps, "create_session"),
                    patch.object(apps, "search_repositories", return_value=[raw]),
                    patch.object(apps.time, "sleep"),
                ):
                    apps.main()
                saved = apps.parse_markdown_entries(path)
                self.assertIn(LEGEND, path.read_text(encoding="utf-8"))
                marked = next(repo for repo in saved if repo["full_name"].casefold() == "owner/marked")
                self.assertTrue(marked["inactivity_marker"])
                self.assertEqual(marked["stars"], 2200)
                self.assertEqual(len(saved), 2 if append else 1)


if __name__ == "__main__":
    unittest.main()
