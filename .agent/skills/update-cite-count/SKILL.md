---
name: update-cite-count
description: "Update citation counts for papers in the ranked sections of section/best_practices.md with update_citation_counts.py. USE FOR: refreshing counts. DO NOT USE FOR: adding papers or classifying entries."
---

The script refreshes Semantic Scholar counts in place for the `RAG Research` and `Agent Research` sections (ranked by cite count >=100). It does not add papers.

```powershell
.venv\Scripts\python.exe code/update_citation_counts.py --dry-run
.venv\Scripts\python.exe code/update_citation_counts.py
```

Afterwards, check `section/best_practices.md` and manually reorder entries if the ranking changed.
