---
name: add-new-entry-from-temp-md
description: "Format new entries from temp.md into temp_entries.md, ready to insert into the section files. USE FOR: adding new resources to the knowledge base. DO NOT USE FOR: editing existing entries or restructuring sections."
---

`temp.md` is a raw checklist of URLs and notes. Produce `temp_entries.md`, a staging file grouped under `## <filename> - <Section Name>:` headings. Mark processed items in `temp.md` as `[x]`.

## Steps

1. **Classify** each item into a file (`azure.md`, `applications.md`, `models_research.md`, `best_practices.md`, `tools_extra.md`) and an existing section. Copy the heading text exactly from the target file (`Select-String '^#' section/<file>`). Do not invent sections or add entries to generated files (`x_llm_apps.md`, `x_llm_papers.md`, `x_popular_papers.md`).
2. **Describe**: for GitHub repos run `code/fetch_github_description.py`; for arXiv, blogs, and product pages read the page and write one sentence (15 words or fewer, do not repeat the name).
3. **Date**: for GitHub repos run `code/update_github_dates.py`; for arXiv derive from the ID prefix (`2602.x` = Feb 2026); for blogs use the page date.
4. **Stars**: run `code/add_github_stars.py` on `github.com` links only.

```powershell
python code/fetch_github_description.py --input temp.md --output temp_with_desc.md
python code/update_github_dates.py --input temp_with_desc.md --in-place
python code/add_github_stars.py --input temp_with_desc.md --in-place
```

## Format

| File | Line |
|------|------|
| `azure.md` | `- [Name](url) - Description. (Mon YYYY) ![stars](...)` (no emoji markers) |
| others | `1. [Name📑](url): Description. [Mon YYYY] ![stars](...)` (use `-` if the section uses dashes) |

- Symbol goes inside the link text right after the name: 📑 paper, 📺 video, 🤗 Hugging Face, none for blogs/docs.
- Star badge goes last, and only on `github.com` links.
- Preserve existing symbols when editing.
