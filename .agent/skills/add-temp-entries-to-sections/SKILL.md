---
name: add-temp-entries-to-sections
description: "Insert formatted entries from temp_entries.md into the section files. USE FOR: moving staged entries into section/*.md. DO NOT USE FOR: creating entries in temp_entries.md or moving entries between sections."
---

Each entry in `temp_entries.md` sits under a `## <filename> - <Section Name>:` heading.

1. Insert the entry under that exact heading in `section/<filename>`.
2. Keep the section's alphabetical order and existing format.
3. Mark the entry in `temp_entries.md` with ✅.

Never insert into generated files (`x_llm_apps.md`, `x_llm_papers.md`, `x_popular_papers.md`); use the matching fetch skill instead.
