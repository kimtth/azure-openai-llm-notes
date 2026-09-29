---
name: fetch-llm-papers
description: "Refresh the LLM landscape paper pool (section/x_llm_papers.md) with fetch_llm_papers.py. USE FOR: refreshing citation counts or expanding topic coverage. DO NOT USE FOR: hand-curated entries (use add-new-entry-from-temp-md) or best_practices.md citation counts (use update-cite-count)."
---

`section/x_llm_papers.md` is a generated list of CS papers with at least 150 citations, ranked by citation count via Semantic Scholar. `models_research.md` links to it. Do not edit it by hand.

## Commands

```powershell
# Routine refresh of existing papers (no search queries)
.venv\Scripts\python.exe code/fetch_llm_papers.py --refresh-existing --min-citations 150

# Full re-fetch of all topics (required after editing TOPICS)
.venv\Scripts\python.exe code/fetch_llm_papers.py --reset --min-citations 150 --top-n 50

# Resume after a 429 or [pause]: rerun WITHOUT --reset
.venv\Scripts\python.exe code/fetch_llm_papers.py --min-citations 150 --top-n 50

# Re-tag topics locally, no API calls
.venv\Scripts\python.exe code/fetch_llm_papers.py --annotate-existing --min-citations 150

# Only some topics (substring match)
.venv\Scripts\python.exe code/fetch_llm_papers.py --topics "PEFT" "Reasoning"
```

Set `$env:S2_API_KEY` if available. On rate limits, lower `--batch-size` or raise `--request-delay`. Run with `--help` for other options.

## Topics

Defined in the `TOPICS` dict in `code/fetch_llm_papers.py` (topic label to list of search queries). Use 4-8 word descriptive phrases, avoid the word "survey", and pair broad terms with LLM-relevance words. After editing, run with `--reset`.

## Notes

- Entry format: `N. [Title📑](url): Abstract sentence. [Mon YYYY] (Citations: N; Topics: A, B)`.
- Progress is saved in `section/x_llm_papers.checkpoint.json`, deleted on success. Delete it manually if corrupted.
- Never add a topic to `completed_topics` by hand after a failure.
