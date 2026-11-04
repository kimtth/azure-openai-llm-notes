---
name: land-section-entries
description: "Classify and format resources from temp.md into temp_entries.md; insert staged entries into section/*.md only on explicit request. Use for staging or landing new knowledge-base entries, not restructuring sections or refreshing generated lists."
---

# Land Section Entries

Flow (Git analogy): `temp.md` = workspace → `temp_entries.md` = staging → `section/*.md` = remote origin. No Git commit or push is implied.

**Guardrail:** Default to staging only. Never modify section files without an explicit user request to insert or land entries. Skill invocation or staging requests are not permission. Ask if landing intent is ambiguous; skip staging for land-only requests.

Preserve existing edits and staging records. Report missing or empty inputs; never invent resources or clear checklists.

## Stage

1. Process unchecked items in `temp.md`; deduplicate against staging and destination sections.
2. Choose `azure.md`, `applications.md`, `models_research.md`, `best_practices.md`, or `tools_extra.md`. Copy an existing section's heading text exactly (`Select-String -Path 'section\<filename>' -Pattern '^#'`).
3. Group staged entries under `## <filename> - <Section Name>:` headings.
4. Verify sources; write a sentence of at most 15 words without repeating the name. Use the GitHub helpers below for repository descriptions, creation dates, and star badges. Read other sources directly.
5. Date arXiv entries by ID prefix (`2602.x` = Feb 2026), blogs by publication date. Omit unknown dates; distinguish documentation updates from releases.
6. Mark successfully staged source items `[x]` (not landed). Leave unresolved items unchecked in both files with a brief blocker; never guess names, dates, or comparison claims.

### GitHub metadata

Prepare temporary `[Name](https://github.com/owner/repo):` lines; bare URLs are unsupported. Run from the repository root:

```powershell
python code\fetch_github_description.py --input <prepared-links.md> --output <metadata.md>
python code\update_github_dates.py --input <metadata.md> --in-place
python code\add_github_stars.py --input <metadata.md> --in-place
```

Merge verified metadata, then remove temporary files. For subpaths or trailing slashes, fetch parent-repository metadata but preserve resource URLs. Add badges only for GitHub repositories, never organization pages.

## Format

| Destination | Entry |
|-------------|-------|
| `azure.md` | `- [Name](url) - Description. (Mon YYYY) ![stars](...)` (no emoji) |
| Others | `1. [Name📑](url): Description. [Mon YYYY] ![stars](...)` (use dashes where the section does) |

Put symbols inside link text after the name: 📑 paper, 📺 video, 🤗 Hugging Face; none for blogs/docs. Preserve existing symbols. Omit unavailable dates and inapplicable badges; repository badges go last.

## Land (explicit request only)

1. Match each staged group's exact destination heading. Skip unresolved and ✅ entries.
2. Insert verified entries alphabetically, matching existing formatting and removing staging-only markers/notes. Never duplicate or silently overwrite existing resources.
3. Confirm each resource exists in the correct section, then mark its staged entry ✅, including resources already present. Retain both checklists.

## Verify

- Never hand-edit generated `x_llm_apps.md`, `x_llm_papers.md`, or `x_popular_papers.md`; use the matching fetch workflow.
- Check headings, source coverage, duplicates, description length, dates, badges, and checklist state. Confirm landed entries exist in their intended sections.
- Report staged/landed results and blockers. Without explicit landing permission, section files must remain unchanged.
