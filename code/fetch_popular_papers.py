"""Collect foundational LLM, RAG, and agent papers from Semantic Scholar.

Foundational papers are resolved by stable arXiv IDs in both discovery and
--refresh-existing mode, which otherwise only revisits the existing entries.
Search results are ranked by citations at the API, not just within a relevance page.

Monthly use: run normally for discovery, or use --refresh-existing for citation
counts only. Successful responses persist in .cache/semantic-scholar for the
current UTC month. Repeating a command retries only uncached requests. Both paper
scripts share request pacing and cooldowns; run them sequentially.
"""

from __future__ import annotations

import argparse
import os
import random
import re
import time
from datetime import UTC, datetime
from pathlib import Path

import requests
from utils.http_utils import create_session
from utils.path_utils import get_repo_root
from utils.semantic_scholar import RateLimitDeferred, SemanticScholarSession


FOUNDATION_TOPIC = "Foundational LLMs & Transformers"
FOUNDATION_IDS = [
    "ARXIV:1706.03762",  # Attention Is All You Need
    "ARXIV:1810.04805",  # BERT
    "ARXIV:1910.10683",  # T5
    "ARXIV:2005.14165",  # GPT-3
    "ARXIV:2203.02155",  # InstructGPT
    "ARXIV:2302.13971",  # LLaMA
    "ARXIV:2307.09288",  # Llama 2
]
OUTPUT_TITLE = "# Popular Papers on Foundational LLMs, RAG & AI Agents (Computer Science)"


def infer_arxiv_date(arxiv_id: str) -> tuple[int, int] | None:
    """Infer (year, month) from arXiv ID (YYMM.NNNNN format)."""
    match = re.match(r'(\d{2})(\d{2})\.(\d{4,5})', arxiv_id)
    if not match:
        return None
    yy, mm = int(match.group(1)), int(match.group(2))
    year = 2000 + yy if yy <= 99 else yy
    if not (1 <= mm <= 12 and 1991 <= year <= datetime.now(UTC).year + 1):
        return None
    return year, mm

def format_month_year(year: int, month: int) -> str:
    """Format as [Mon YYYY]"""
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    return f"[{months[month-1]} {year}]"

class SemanticScholarFetcher:
    """Fetch popular papers from Semantic Scholar API."""

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(
        self,
        *,
        user_agent: str | None,
        api_key: str | None,
        timeout: int,
        max_retries: int,
        backoff: float,
        request_delay: float,
        jitter: float,
        cache_dir: Path | None = None,
    ):
        self.session = (
            SemanticScholarSession(cache_dir, request_delay=request_delay, jitter=jitter, user_agent=user_agent)
            if cache_dir is not None else create_session(user_agent)
        )
        if api_key:
            self.session.headers.update({"x-api-key": api_key})
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff
        self.request_delay = request_delay
        self.jitter = jitter
        # Pace every request, including the first, for unauthenticated API use.
        self._next_request_at = 0.0

    def _wait_for_request_slot(self) -> None:
        if isinstance(self.session, SemanticScholarSession):
            return
        wait = self._next_request_at - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._next_request_at = (
            time.monotonic()
            + max(self.request_delay, 1.0)
            + random.uniform(0, max(self.jitter, 0))
        )

    def _defer_after_rate_limit(self, backoff: float) -> None:
        self._next_request_at = max(
            self._next_request_at,
            time.monotonic() + backoff + random.uniform(0, max(self.jitter, 0)),
        )

    def search_papers(self, query: str, limit: int = 50, fields: list[str] | None = None) -> list[dict]:
        """Search papers by query and return results."""
        if fields is None:
            fields = [
                "paperId",
                "title",
                "authors",
                "year",
                "citationCount",
                "abstract",
                "venue",
                "url",
                "externalIds",
                "fieldsOfStudy",
            ]

        params = {
            "query": query,
            "fields": ",".join(fields),
            "sort": "citationCount:desc",
            "fieldsOfStudy": "Computer Science",
        }

        url = f"{self.BASE_URL}/paper/search/bulk"
        backoff = self.backoff
        last_error = "no response"
        last_status = None

        for attempt in range(self.max_retries):
            try:
                self._wait_for_request_slot()
                response = self.session.get(url, params=params, timeout=self.timeout)
            except requests.RequestException as exc:
                last_status = None
                last_error = f"{type(exc).__name__}: {exc}"
            else:
                last_status = response.status_code
                if response.status_code == 200:
                    return response.json().get("data", [])[:limit]

                message = ""
                try:
                    payload = response.json()
                    message = str(payload.get("message") or payload.get("error") or "").strip()
                except ValueError:
                    message = response.text[:200].strip()
                last_error = f"HTTP {response.status_code}"
                if message:
                    last_error += f": {message}"

                if response.status_code not in {429, 500, 502, 503, 504}:
                    break

                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        backoff = max(backoff, float(retry_after))
                    except ValueError:
                        pass
                elif response.status_code == 429:
                    backoff = max(backoff, 120.0)
                    self._defer_after_rate_limit(backoff)

            if attempt < self.max_retries - 1:
                time.sleep(backoff)
                backoff = min(backoff * 2, 300.0)

        error = RateLimitDeferred if last_status == 429 else RuntimeError
        raise error(f"Semantic Scholar query failed after retries ({last_error}): {query}")

    def batch_papers(self, ids: list[str], fields: list[str] | None = None) -> list[dict | None]:
        """Fetch papers by stable IDs in one low-volume API request."""
        if fields is None:
            fields = [
                "paperId",
                "title",
                "authors",
                "year",
                "citationCount",
                "abstract",
                "venue",
                "url",
                "externalIds",
                "fieldsOfStudy",
            ]

        if not ids:
            return []

        url = f"{self.BASE_URL}/paper/batch"
        params = {"fields": ",".join(fields)}
        backoff = self.backoff
        last_error = "no response"

        for attempt in range(self.max_retries):
            try:
                self._wait_for_request_slot()
                response = self.session.post(url, params=params, json={"ids": ids}, timeout=self.timeout)
            except requests.RequestException as exc:
                last_error = f"{type(exc).__name__}: {exc}"
            else:
                if response.status_code == 200:
                    return response.json()

                message = ""
                try:
                    payload = response.json()
                    message = str(payload.get("message") or payload.get("error") or "").strip()
                except ValueError:
                    message = response.text[:200].strip()
                last_error = f"HTTP {response.status_code}"
                if message:
                    last_error += f": {message}"

                if response.status_code not in {429, 500, 502, 503, 504}:
                    break

                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        backoff = max(backoff, float(retry_after))
                    except ValueError:
                        pass
                elif response.status_code == 429:
                    backoff = max(backoff, 120.0)
                    self._defer_after_rate_limit(backoff)

            if attempt < self.max_retries - 1:
                time.sleep(backoff)
                backoff = min(backoff * 2, 300.0)

        raise RuntimeError(f"Semantic Scholar batch fetch failed after retries ({last_error})")

    def get_paper(self, paper_id: str, fields: list[str]) -> dict | None:
        """Fetch a single paper when the batch endpoint is rate limited."""
        url = f"{self.BASE_URL}/paper/{paper_id}"
        params = {"fields": ",".join(fields)}
        backoff = self.backoff

        for attempt in range(self.max_retries):
            try:
                self._wait_for_request_slot()
                response = self.session.get(url, params=params, timeout=self.timeout)
            except requests.RequestException:
                response = None

            if response is not None and response.status_code == 200:
                return response.json()

            if response is None or response.status_code not in {429, 500, 502, 503, 504}:
                return None

            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    backoff = max(backoff, float(retry_after))
                except ValueError:
                    pass
            elif response.status_code == 429:
                backoff = max(backoff, 120.0)
                self._defer_after_rate_limit(backoff)

            if attempt < self.max_retries - 1:
                time.sleep(backoff)
                backoff = min(backoff * 2, 300.0)

        return None

    def get_papers_sorted_by_citations(self, query: str, top_n: int = 30, min_citations: int = 100) -> list[dict]:
        """Get top N papers sorted by citation count."""
        papers = self.search_papers(query, limit=100)

        cs_papers = [
            p
            for p in papers
            if p.get("fieldsOfStudy")
            and "Computer Science" in p.get("fieldsOfStudy", [])
            and p.get("citationCount", 0) >= min_citations
        ]

        sorted_papers = sorted(cs_papers, key=lambda x: x.get("citationCount", 0), reverse=True)
        return sorted_papers[:top_n]


def format_paper_info(paper: dict, rank: int) -> str:
    """Format paper information for display"""
    authors = paper.get('authors', [])
    author_names = ', '.join([a.get('name', '') for a in authors[:3]])
    if len(authors) > 3:
        author_names += ', et al.'
    
    external_ids = paper.get('externalIds', {})
    arxiv_id = external_ids.get('ArXiv') if external_ids else None
    arxiv_url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None
    
    year_month_str = ""
    if arxiv_id:
        ym = infer_arxiv_date(arxiv_id)
        if ym:
            year_month_str = format_month_year(ym[0], ym[1])
    
    lines = [
        f"\n{rank}. {paper.get('title', 'No title')}",
        f"   Authors: {author_names}",
        f"   Year: {paper.get('year', 'N/A')} | Citations: {paper.get('citationCount', 0):,} | Venue: {paper.get('venue', 'N/A')}"
    ]
    
    if year_month_str:
        lines.append(f"   Year Month: {year_month_str}")
    if paper.get('fieldsOfStudy'):
        lines.append(f"   Fields: {', '.join(paper['fieldsOfStudy'])}")
    lines.append(f"   URL: {paper.get('url', 'N/A')}")
    if arxiv_url:
        lines.append(f"   arXiv: {arxiv_url}")
    
    return '\n'.join(lines) + '\n'


def save_to_markdown(topic: str, papers: list[dict], filename: str) -> None:
    """Save papers to a markdown file"""
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"\n## {topic}\n\n*Retrieved: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        for idx, paper in enumerate(papers, 1):
            authors = paper.get('authors', [])
            author_names = ', '.join([a.get('name', '') for a in authors[:3]])
            if len(authors) > 3:
                author_names += ', et al.'
            
            external_ids = paper.get('externalIds', {})
            arxiv_id = external_ids.get('ArXiv') if external_ids else None
            arxiv_url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None
            
            year_month_str = ""
            if arxiv_id:
                ym = infer_arxiv_date(arxiv_id)
                if ym:
                    year_month_str = format_month_year(ym[0], ym[1])
            
            f.write(f"### {idx}. {paper.get('title', 'No title')}\n\n")
            f.write(f"**Authors:** {author_names}  \n")
            f.write(f"**Year:** {paper.get('year', 'N/A')} | **Citations:** {paper.get('citationCount', 0):,} | **Venue:** {paper.get('venue', 'N/A')}  \n")
            
            if year_month_str:
                f.write(f"**Year Month:** {year_month_str}  \n")
            if paper.get('fieldsOfStudy'):
                f.write(f"**Fields:** {', '.join(paper['fieldsOfStudy'])}  \n")
            
            url = paper.get('url', 'N/A')
            f.write(f"**URL:** [{url}]({url})  \n")
            if arxiv_url:
                f.write(f"**arXiv:** [{arxiv_url}]({arxiv_url})  \n")
            
            if paper.get('abstract'):
                f.write(f"\n**Abstract:** {paper['abstract']}\n\n")
            f.write("---\n\n")


def paper_lookup_id(paper: dict) -> str | None:
    external_ids = paper.get("externalIds") or {}
    arxiv_id = external_ids.get("ArXiv")
    if arxiv_id:
        return f"ARXIV:{arxiv_id}"
    url = paper.get("url") or ""
    if "arxiv.org/abs/" in url:
        return "ARXIV:" + url.rsplit("/abs/", 1)[1].strip()
    if "semanticscholar.org/paper/" in url:
        return url.rsplit("/paper/", 1)[1].split("/", 1)[0].strip()
    return None


def fetch_foundational_papers(
    fetcher: SemanticScholarFetcher,
    min_citations: int,
    existing: list[dict] | None = None,
) -> list[dict]:
    known = {paper_lookup_id(paper): paper for paper in existing or []}
    missing_ids = [identifier for identifier in FOUNDATION_IDS if identifier not in known]
    known_ids = [identifier for identifier in FOUNDATION_IDS if identifier in known]
    for identifiers, fields in [(missing_ids, None), (known_ids, ["citationCount"])]:
        if not identifiers:
            continue
        records = (
            fetcher.batch_papers(identifiers) if fields is None
            else fetcher.batch_papers(identifiers, fields=fields)
        )
        if len(records) != len(identifiers):
            raise RuntimeError("Could not resolve every foundational paper; leaving output unchanged.")
        for identifier, record in zip(identifiers, records):
            if record is None:
                raise RuntimeError("Could not resolve every foundational paper; leaving output unchanged.")
            known[identifier] = {**known.get(identifier, {}), **record}
    papers = [known[identifier] for identifier in FOUNDATION_IDS]
    filtered = [
        paper for paper in papers
        if paper is not None
        and paper.get("citationCount", 0) >= min_citations
        and "Computer Science" in (paper.get("fieldsOfStudy") or [])
    ]
    return sorted(filtered, key=lambda paper: paper.get("citationCount", 0), reverse=True)


def parse_existing_markdown(filename: str) -> list[tuple[str, list[dict]]]:
    text = Path(filename).read_text(encoding="utf-8")
    sections: list[tuple[str, list[dict]]] = []
    section_re = re.compile(r"^## (.+?)\n\n\*Retrieved: [^*]+\*\n\n(.*?)(?=^## |\Z)", re.DOTALL | re.MULTILINE)
    entry_re = re.compile(r"^### \d+\. (.+?)\n\n(.*?)(?=^### \d+\. |\Z)", re.DOTALL | re.MULTILINE)

    for section_match in section_re.finditer(text):
        topic_name = section_match.group(1)
        papers: list[dict] = []
        for entry_match in entry_re.finditer(section_match.group(2)):
            title = entry_match.group(1).strip()
            block = entry_match.group(2)
            citation_match = re.search(r"\*\*Citations:\*\* ([\d,]+)", block)
            year_match = re.search(r"\*\*Year:\*\* (\d{4}|N/A)", block)
            venue_match = re.search(r"\| \*\*Venue:\*\*([^\n]+)", block)
            fields_match = re.search(r"\*\*Fields:\*\*([^\n]+)", block)
            url_match = re.search(r"\*\*URL:\*\* \[([^\]]+)\]", block)
            arxiv_match = re.search(r"\*\*arXiv:\*\* \[https://arxiv\.org/abs/([^\]]+)\]", block)
            abstract_match = re.search(r"\*\*Abstract:\*\* (.*?)(?:\n\n---|\Z)", block, re.DOTALL)
            authors_match = re.search(r"\*\*Authors:\*\*([^\n]+)", block)

            external_ids = {"ArXiv": arxiv_match.group(1)} if arxiv_match else {}
            papers.append({
                "title": title,
                "authors": [{"name": name.strip()} for name in (authors_match.group(1).split(",") if authors_match else [])],
                "year": None if not year_match or year_match.group(1) == "N/A" else int(year_match.group(1)),
                "citationCount": int(citation_match.group(1).replace(",", "")) if citation_match else 0,
                "venue": venue_match.group(1).strip() if venue_match else "",
                "url": url_match.group(1).strip() if url_match else "",
                "externalIds": external_ids,
                "fieldsOfStudy": [field.strip() for field in fields_match.group(1).split(",")] if fields_match else [],
                "abstract": " ".join(abstract_match.group(1).split()) if abstract_match else "",
            })
        sections.append((topic_name, papers))
    return sections


def refresh_existing_markdown(
    fetcher: SemanticScholarFetcher,
    filename: str,
    min_citations: int,
    batch_size: int,
) -> None:
    sections = parse_existing_markdown(filename)
    if not sections or not any(papers for _, papers in sections):
        raise RuntimeError(f"No paper sections found in {filename}; leaving output unchanged.")
    existing_foundations = {
        paper_lookup_id(paper)
        for topic, entries in sections if topic == FOUNDATION_TOPIC for paper in entries
    }
    if set(FOUNDATION_IDS).issubset(existing_foundations):
        foundations = []
    else:
        foundations = fetch_foundational_papers(
            fetcher, min_citations,
            [paper for topic, entries in sections if topic == FOUNDATION_TOPIC for paper in entries],
        )
    if not any(topic == FOUNDATION_TOPIC for topic, _ in sections):
        sections.insert(0, (FOUNDATION_TOPIC, []))
    lookup_ids = list(dict.fromkeys(
        paper_lookup_id(paper) for _, papers in sections for paper in papers
        if paper_lookup_id(paper)
    ))
    live_by_id: dict[str, dict | None] = {}

    for start in range(0, len(lookup_ids), batch_size):
        chunk = [paper_id for paper_id in lookup_ids[start:start + batch_size] if paper_id]
        if not chunk:
            continue
        print(f"[batch] Fetching {len(chunk)} papers ({start + 1}-{start + len(chunk)})")
        live_by_id.update(zip(chunk, fetcher.batch_papers(chunk, fields=["citationCount"])))

    refreshed_sections: list[tuple[str, list[dict]]] = []
    changed = 0
    missing = 0
    for topic_name, papers in sections:
        refreshed = []
        for paper in papers:
            lookup_id = paper_lookup_id(paper)
            live = live_by_id.get(lookup_id or "")
            if live:
                if live.get("citationCount") != paper.get("citationCount"):
                    changed += 1
                refreshed.append({**paper, **live})
            else:
                missing += 1
                refreshed.append(paper)
        if topic_name == FOUNDATION_TOPIC:
            by_id = {paper_lookup_id(paper): paper for paper in refreshed}
            by_id.update({paper_lookup_id(paper): paper for paper in foundations})
            refreshed = list(by_id.values())
        filtered = [
            paper for paper in refreshed
            if paper.get("citationCount", 0) >= min_citations
            and "Computer Science" in (paper.get("fieldsOfStudy") or [])
        ]
        filtered.sort(key=lambda paper: paper.get("citationCount", 0), reverse=True)
        refreshed_sections.append((topic_name, filtered))

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{OUTPUT_TITLE}\n\n")
        f.write(f"*Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}*\n")
        f.write("*Source: Semantic Scholar batch API refresh of existing paper IDs*\n")
        f.write("*Filtered for Computer Science papers only*\n")
        f.write("*Includes foundational LLM papers resolved by stable arXiv IDs.*\n")
        if missing:
            f.write(f"*Warning: {missing} existing entries could not be refreshed and retain previously recorded data.*\n")

    for topic_name, papers in refreshed_sections:
        save_to_markdown(topic_name, papers, filename)

    print(
        f"Refreshed {sum(len(papers) for _, papers in refreshed_sections)} existing papers from Semantic Scholar batch API: "
        f"{changed} citation count(s) changed, {missing} missing response(s)."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch foundational LLM and top-cited RAG/agent papers from Semantic Scholar.")
    parser.add_argument("--output", help="Output markdown file path.")
    parser.add_argument("--min-citations", type=int, default=100, help="Minimum citation threshold.")
    parser.add_argument("--top-n", type=int, default=30, help="Top N papers per query.")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds.")
    parser.add_argument("--max-retries", type=int, default=5, help="Max retries for API calls.")
    parser.add_argument("--backoff", type=float, default=1.0, help="Initial backoff in seconds.")
    parser.add_argument(
        "--request-delay", type=float, default=5.0,
        help="Delay between Semantic Scholar requests in seconds (default: 5)."
    )
    parser.add_argument(
        "--jitter", type=float, default=0.5,
        help="Random extra delay between requests in seconds."
    )
    parser.add_argument(
        "--api-key-env", default="S2_API_KEY",
        help="Environment variable containing a Semantic Scholar API key, if available."
    )
    parser.add_argument(
        "--refresh-existing", action="store_true",
        help="Refresh citation counts only, preserving existing metadata and skipping discovery."
    )
    parser.add_argument(
        "--batch-size", type=int, default=20,
        help="Number of papers per refresh request (default: 20)."
    )
    parser.add_argument("--cache-dir", type=Path, help="Shared monthly API cache (default: .cache/semantic-scholar).")
    parser.add_argument("--user-agent", default="Academic-Research-Tool/1.0", help="Custom User-Agent.")
    args = parser.parse_args()
    if args.batch_size < 1 or args.top_n < 1 or args.min_citations < 0:
        parser.error("--batch-size and --top-n must be positive; --min-citations must be non-negative.")
    if args.max_retries < 1 or args.request_delay < 1 or args.jitter < 0 or args.backoff < 0:
        parser.error("--max-retries and --request-delay must be at least 1; --jitter and --backoff must be non-negative.")

    root_dir = get_repo_root(__file__)
    fetcher = SemanticScholarFetcher(
        user_agent=args.user_agent,
        api_key=os.environ.get(args.api_key_env),
        timeout=args.timeout,
        max_retries=args.max_retries,
        backoff=args.backoff,
        request_delay=args.request_delay,
        jitter=args.jitter,
        cache_dir=args.cache_dir or root_dir / ".cache" / "semantic-scholar",
    )

    output_file = args.output or str(root_dir / "section" / "x_popular_papers.md")

    if args.refresh_existing:
        refresh_existing_markdown(fetcher, output_file, args.min_citations, args.batch_size)
        return

    topics = {
        "RAG (Retrieval-Augmented Generation)": [
            '"retrieval-augmented generation"',
            '"RAG" "language models"',
            '"retrieval augmented generation"',
            '"retrieval augmented" "language models"',
        ],
        "AI Agents": [
            '"AI agents" "language models"',
            '"LLM agents"',
            '"language model" "agents"',
            '"LLM agent"',
        ]
    }
    
    existing_foundations = [
        paper for topic, entries in parse_existing_markdown(output_file) if topic == FOUNDATION_TOPIC
        for paper in entries
    ] if Path(output_file).exists() else []
    topic_papers = [(FOUNDATION_TOPIC, fetch_foundational_papers(fetcher, args.min_citations, existing_foundations))]
    failed_searches: list[str] = []
    for topic_name, queries in topics.items():
        print(f"\nTopic: {topic_name}")
        
        all_papers = []
        seen_ids = set()
        failed_queries = []
        for query in queries:
            try:
                query_papers = fetcher.get_papers_sorted_by_citations(query, top_n=args.top_n, min_citations=args.min_citations)
            except RateLimitDeferred as exc:
                raise RateLimitDeferred(
                    f"{exc}. Discovery paused; successful responses are saved in the monthly cache. "
                    "Re-run this command later to resume. Existing Markdown is unchanged."
                ) from exc
            except RuntimeError as exc:
                failed_queries.append(str(exc))
                failed_searches.append(query)
                print(f"  [WARN] {exc}")
                continue

            for paper in query_papers:
                paper_id = paper.get('paperId')
                if paper_id and paper_id not in seen_ids:
                    seen_ids.add(paper_id)
                    all_papers.append(paper)
        
        # Filter and sort
        filtered_papers = [p for p in all_papers if p.get('citationCount', 0) >= args.min_citations]
        filtered_papers.sort(key=lambda x: x.get('citationCount', 0), reverse=True)
        filtered_papers = filtered_papers[:args.top_n]
        if not filtered_papers:
            if failed_queries:
                print("\n".join(f"  [ERROR] {error}" for error in failed_queries))
            raise RuntimeError(
                f"No papers found for {topic_name}. The API may be unavailable or rate limited; "
                "leaving the existing output file unchanged."
            )
        topic_papers.append((topic_name, filtered_papers))
        
        for idx, paper in enumerate(filtered_papers, 1):
            print(format_paper_info(paper, idx))
        
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{OUTPUT_TITLE}\n\n")
        f.write(f"*Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}*\n")
        f.write("*Filtered for Computer Science papers only*\n")
        f.write("*Includes foundational LLM papers resolved by stable arXiv IDs.*\n")
        if failed_searches:
            f.write(
                f"*Warning: {len(failed_searches)} discovery queries failed; "
                "rankings use the successful queries only.*\n"
            )
    
    for topic_name, filtered_papers in topic_papers:
        save_to_markdown(topic_name, filtered_papers, output_file)
        print(f"Saved {len(filtered_papers)} papers")
    
    print(f"\nResults saved to: {output_file}")
    if failed_searches:
        raise RuntimeError(
            f"Partial discovery saved; {len(failed_searches)} queries remain pending. "
            "Re-run this command to resume from the monthly cache."
        )


if __name__ == "__main__":
    main()
