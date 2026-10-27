"""Refresh ranked citations and add qualifying papers from the surrounding sections."""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from fetch_llm_papers import QueryFetchError, SemanticScholarFetcher
from utils.path_utils import get_repo_root
from utils.semantic_scholar import SemanticScholarSession


SECTION_RANGES = (
    ("## **RAG Best Practices**", "## **Agent Best Practices**", "RAG Research (Ranked by cite count >=100)"),
    ("## **Agent Best Practices**", "### **Security and Governance**", "Agent Research (Ranked by cite count >=100)"),
)


def extract_papers_from_ranked_section(content: str, section_name: str) -> list[tuple[str, str, int, str, str]]:
    """Extract papers from a ranked section."""
    section_pattern = f'### \\*\\*{re.escape(section_name)}\\*\\*'
    section_match = re.search(section_pattern, content)
    if not section_match:
        raise ValueError(f"Ranked section not found: {section_name}")
    
    start = section_match.end()
    next_section = re.search(r'\n(?:#{2,3} |---(?:\s|$))', content[start:])
    section_content = content[start:start + next_section.start()] if next_section else content[start:]
    
    paper_pattern = (
        r'^-\s+\[([^\]]*?)📑(?:💡)?\]\(https://(?:arxiv\.org/abs/'
        r'(?P<arxiv>\d{4}\.\d{4,5})|(?:www\.)?semanticscholar\.org/paper/'
        r'(?P<semantic>[a-fA-F0-9]{40}))\):[^\n]*\(Citations:\s*([\d,]+)\)'
    )
    papers = []
    for match in re.finditer(paper_pattern, section_content, re.MULTILINE):
        identifier = f"ARXIV:{match.group('arxiv')}" if match.group("arxiv") else match.group("semantic")
        count_text = match.group(4)
        papers.append((match.group(1), identifier, int(count_text.replace(",", "")), count_text, match.group(0)))
    citation_lines = re.findall(r"^.*\(Citations:\s*[\d,]+\).*$", section_content, re.MULTILINE)
    if len(citation_lines) != len(papers):
        raise ValueError(f"{section_name} contains citation entries with unsupported or malformed links.")
    return papers


def extract_source_papers(content: str, start_heading: str, end_heading: str) -> list[tuple[str, str]]:
    """Return source paper IDs and normalized entries outside the ranked sections."""
    start = content.find(start_heading)
    end = content.find(end_heading, start + len(start_heading)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Could not find source section between {start_heading!r} and {end_heading!r}.")
    block = content[start + len(start_heading):end]
    block = re.sub(
        r"### \*\*(?:RAG|Agent) Research \(Ranked by cite count >=100\)\*\*[\s\S]*?(?=\n### |\n## |\Z)",
        "", block,
    )
    papers: list[tuple[str, str]] = []
    for line in block.splitlines():
        match = re.match(r"^\s*(?:>\s*)?-\s+\[([^\]]*📑(?:💡)?)\]\(([^)]+)\)(.*)$", line)
        if not match:
            continue
        title, link, description = match.groups()
        arxiv = re.fullmatch(r"https://arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})(?:\.pdf)?", link)
        semantic = re.fullmatch(r"https://(?:www\.)?semanticscholar\.org/paper/([a-fA-F0-9]{40})", link)
        if arxiv:
            identifier = f"ARXIV:{arxiv.group(1)}"
            link = f"https://arxiv.org/abs/{arxiv.group(1)}"
        elif semantic:
            identifier = semantic.group(1)
        else:
            raise ValueError(f"Paper link cannot be used for citation lookup: {link}")
        description = description.strip()
        if description.startswith(":"):
            description = description[1:].strip()
        elif description.startswith("- "):
            description = description[2:].strip()
        papers.append((identifier, f"- [{title}]({link}): {description}".rstrip()))
    return papers


def add_ranked_entries(content: str, section_name: str, entries: list[str]) -> str:
    if not entries:
        return content
    heading = f"### **{section_name}**"
    start = content.index(heading) + len(heading)
    following = re.search(r"\n(?:#{2,3} |---(?:\s|$))", content[start:])
    end = start + following.start() if following else len(content)
    separator = "" if content[:end].endswith("\n") else "\n"
    return content[:end] + separator + "\n".join(entries) + "\n" + content[end:]


def sort_ranked_section(content: str, section_name: str) -> str:
    """Sort a ranked section in descending citation-count order."""
    section_pattern = f'### \\*\\*{re.escape(section_name)}\\*\\*'
    section_match = re.search(section_pattern, content)
    if not section_match:
        return content

    start = section_match.end()
    next_section = re.search(r'\n(?:#{2,3} |---(?:\s|$))', content[start:])
    end = start + next_section.start() if next_section else len(content)
    section_lines = content[start:end].splitlines(keepends=True)
    citation_lines = [
        line for line in section_lines
        if re.search(r'\(Citations:\s*[\d,]+\)', line)
    ]
    sorted_citation_lines = sorted(
        citation_lines,
        key=lambda line: int(re.search(r'\(Citations:\s*([\d,]+)\)', line).group(1).replace(",", "")),
        reverse=True,
    )
    citation_line_iter = iter(sorted_citation_lines)
    sorted_section = "".join(
        next(citation_line_iter) if line in citation_lines else line
        for line in section_lines
    )
    return content[:start] + sorted_section + content[end:]

def update_ranked_sections(
    file_path: Path,
    *,
    timeout: int,
    max_retries: int,
    sleep_s: float,
    dry_run: bool,
    sort_only: bool,
) -> int:
    """Update citation counts in ranked sections."""

    content = file_path.read_text(encoding="utf-8")
    
    sections = [ranked for _, _, ranked in SECTION_RANGES]
    
    papers = [paper for section in sections for paper in extract_papers_from_ranked_section(content, section)]
    if not papers:
        raise ValueError(f"No ranked citation entries found in {file_path}.")
    replacements = []
    failure: QueryFetchError | None = None
    missing: list[str] = []
    additions: dict[str, list[str]] = {section: [] for section in sections}
    if not sort_only:
        sources = {
            ranked: extract_source_papers(content, start, end)
            for start, end, ranked in SECTION_RANGES
        }
        ids = list(dict.fromkeys(
            [paper[1] for paper in papers] +
            [identifier for entries in sources.values() for identifier, _ in entries]
        ))
        fetcher = SemanticScholarFetcher(
            user_agent="awesome-azure-openai-llm/1.0", api_key=None,
            timeout=timeout, max_retries=max_retries, backoff=max(1.0, sleep_s),
            request_delay=max(1.0, sleep_s), jitter=0,
            cache_dir=get_repo_root(__file__) / ".cache" / "semantic-scholar",
        )
        try:
            if not isinstance(fetcher.session, SemanticScholarSession):
                raise TypeError("Citation refresh requires the shared Semantic Scholar cache.")
            cached = fetcher.session.cached_papers(ids, ["citationCount"])
            results: dict[str, dict | None] = dict(cached)
            pending = [identifier for identifier in ids if identifier not in cached]
            print(f"[cache] {len(cached)} IDs from the current UTC month; {len(pending)} to fetch.")
            for start in range(0, len(pending), 500):
                chunk = pending[start:start + 500]
                try:
                    fetched = fetcher.batch_papers(chunk, fields=["citationCount"])
                except QueryFetchError as exc:
                    failure = exc
                    break
                results.update(zip(chunk, fetched))
        finally:
            fetcher.session.close()

        for title, identifier, current_citations, count_text, original_text in papers:
            result = results.get(identifier)
            if result is None:
                continue
            new_citations = result.get("citationCount")
            if not isinstance(new_citations, int) or new_citations < 0:
                raise ValueError(f"Invalid Semantic Scholar citation count for {identifier}.")
            if new_citations != current_citations:
                replacements.append({
                    "old": original_text,
                    "new": original_text.replace(f"(Citations: {count_text})", f"(Citations: {new_citations:,})"),
                    "title": title,
                    "id": identifier,
                    "old_count": current_citations,
                    "new_count": new_citations,
                })
        missing = [identifier for identifier in ids if results.get(identifier) is None]
        for section in sections:
            ranked = extract_papers_from_ranked_section(content, section)
            known_ids = {paper[1] for paper in ranked}
            known_paper_ids = {
                (results.get(identifier) or {}).get("paperId") or identifier for identifier in known_ids
            }
            for identifier, entry in sources[section]:
                result = results.get(identifier)
                if result is None:
                    continue
                count = result.get("citationCount")
                if not isinstance(count, int) or count < 0:
                    raise ValueError(f"Invalid Semantic Scholar citation count for {identifier}.")
                paper_id = result.get("paperId") or identifier
                if count > 100 and identifier not in known_ids and paper_id not in known_paper_ids:
                    additions[section].append(f"{entry} (Citations: {count:,})")
                    known_ids.add(identifier)
                    known_paper_ids.add(paper_id)
        print(
            f"Processed {len(papers)} ranked entries and {len(ids)} unique paper IDs; "
            f"{len(missing)} unavailable."
        )

    updated_content = content
    if replacements:
        print("\nUpdates needed:")
        for i, r in enumerate(replacements, 1):
            print(f"{i}. {r['id']}: {r['old_count']} -> {r['new_count']}")
        
        for r in replacements:
            updated_content = updated_content.replace(r['old'], r['new'])

    for section_name, entries in additions.items():
        updated_content = add_ranked_entries(updated_content, section_name, entries)
    for section_name in sections:
        updated_content = sort_ranked_section(updated_content, section_name)

    if not sort_only:
        month = datetime.datetime.now(datetime.UTC).strftime("%Y-%m")
        status = (
            f"*Citation status: {len(ids) - len(missing)}/{len(ids)} paper IDs checked against Semantic Scholar "
            f"in {month} UTC (including monthly cache); {len(missing)} unavailable."
        )
        if missing:
            status += " Previous counts are retained and qualifying papers may be missing."
        status += "*"
        status_pattern = r"^\*Citation status: [^\n]*\*\n+"
        updated_content = re.sub(status_pattern, "", updated_content, flags=re.MULTILINE)
        title_end = updated_content.find("\n")
        if title_end < 0:
            raise ValueError(f"Cannot insert citation status into {file_path}.")
        updated_content = updated_content[:title_end + 1] + "\n" + status + "\n" + updated_content[title_end + 1:]

    if updated_content == content and not missing:
        print("All up to date")
    elif dry_run:
        print("\nDRY RUN: No files written.")
    elif updated_content != content:
        file_path.write_text(updated_content, encoding="utf-8")
        print(
            f"\nUpdated {len(replacements)} citation counts, added "
            f"{sum(len(entries) for entries in additions.values())} qualifying papers, "
            "and re-sorted ranked sections"
        )

    if missing:
        print(f"[WARN] Citation counts retained for unavailable IDs: {', '.join(missing)}")
        if failure:
            raise QueryFetchError(f"Partial citation refresh: {failure}") from failure
        raise QueryFetchError(f"Partial citation refresh: {len(missing)} paper(s) unavailable.")
    return len(replacements)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Update citation counts in ranked paper sections.")
    parser.add_argument(
        "--file",
        help="Target markdown file (default: section/best_practices.md).",
    )
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds.")
    parser.add_argument("--max-retries", type=int, default=3, help="Max retries for API calls.")
    parser.add_argument("--sleep", type=float, default=10.0, help="Delay between API requests in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Preview updates without writing.")
    parser.add_argument("--sort-only", action="store_true", help="Re-sort ranked sections without calling the API.")
    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    root = get_repo_root(__file__)
    file_path = Path(args.file) if args.file else root / "section" / "best_practices.md"
    update_ranked_sections(
        file_path,
        timeout=args.timeout,
        max_retries=args.max_retries,
        sleep_s=args.sleep,
        dry_run=args.dry_run,
        sort_only=args.sort_only,
    )


if __name__ == "__main__":
    main()
