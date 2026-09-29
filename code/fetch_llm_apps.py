"""Fetch popular LLM applications from GitHub and write a ranked markdown list.

The default output is `section/x_llm_apps.md`, intended to back the
"Popular LLM Applications" link in `section/applications.md`.

Usage:
    python code/fetch_llm_apps.py
    python code/fetch_llm_apps.py --token <GITHUB_TOKEN>
    python code/fetch_llm_apps.py --min-stars 1500
    python code/fetch_llm_apps.py --output files/llm_apps.json
    python code/fetch_llm_apps.py --topics llm ai-agent rag
    python code/fetch_llm_apps.py --search-terms "agent memory" "AI coding agent"
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import UTC, datetime
from importlib import import_module
from pathlib import Path
from typing import Any

import requests

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

create_session = import_module("utils.http_utils").create_session
get_repo_root = import_module("utils.path_utils").get_repo_root


DEFAULT_TOPICS = [
    "llm",
    "large-language-model",
    "agent",
    "agents",
    "ai-agent",
    "rag",
    "retrieval-augmented-generation",
    "langchain",
    "llm-framework",
    "llama-index",
    "openai",
    "chatbot",
    "ai-workflow",
    "prompt-engineering",
    "local-llm",
    "gemini",
    "claude",
    "azure-openai",
    "copilot",
    "assistant",
    "qwen",
    "llama",
    "deepseek",
    "grok",
    "ade",
    "agent-ide",
    "ai-agents",
    "claude-code",
    "codex",
    "cursor-agent",
    "opencode",
    "agentic-ai",
    "multi-agent",
    "mcp",
    "model-context-protocol",
    "a2a",
    "agent2agent",
    "coding-agent",
    "ai-coding-agent",
    "deep-research",
    "research-agent",
    "computer-use",
    "browser-agent",
    "ai-automation",
    "context-engineering",
    "llmops",
    "ai-gateway",
    "model-gateway",
    "prompt-management",
    "graphrag",
    "vector-search",
    "local-ai",
    "voice-agent",
    "ai-engineering",
    "agent-memory",
    "agent-harness",
    "agent-skills",
    "ai-coding-assistant",
    "ai-productivity",
    "agent-orchestration",
    "llm-inference",
    "llm-serving",
    "llm-evaluation",
    "ai-observability",
    "document-ai",
    "ai-image-generation",
    "ai-video-generation",
]

# Phrase searches complement topic tags, which miss repositories that are not
# consistently tagged. The terms reflect broad discovery facets (engineering,
# applications, infrastructure, tutorials, models, and collections) without
# importing or reproducing entries from any external catalog.
DEFAULT_SEARCH_TERMS = [
    "AI agent",
    "agent framework",
    "agent orchestration",
    "agent harness",
    "agent memory",
    "agent skills",
    "AI coding agent",
    "AI coding assistant",
    "AI workflow",
    "AI productivity",
    "personal AI assistant",
    "MCP server",
    "A2A protocol",
    "computer use agent",
    "browser agent",
    "deep research agent",
    "RAG application",
    "GraphRAG",
    "LLM inference",
    "model serving",
    "AI gateway",
    "LLM observability",
    "LLM evaluation",
    "AI image generation",
    "AI video generation",
    "voice agent",
    "AI data analytics",
    "document AI",
]

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
RESULTS_PER_PAGE = 100
MAX_PAGES_PER_QUERY = 10
DEFAULT_USER_AGENT = "awesome-azure-openai-llm/1.0"

RELEVANCE_PATTERN = re.compile(
    r"\b(?:"
    r"llms?|large[- ]language[- ]models?|generative[- ]ai|genai|"
    r"gpt|gpt4free|chatgpt|openai|anthropic|claude|gemini|deepseek|qwen|llama|ollama|"
    r"mistral|whisper|stable diffusion|flux|"
    r"copilot|codex|cursor|vllm|transformers|huggingface|openclaw|openagent|autogpt|"
    r"langchain|llamaindex|browser-use|hermes-agent|deer-flow|paperclip|magentic|openmanus|"
    r"rag|graphrag|retrieval[- ]augmented(?: generation)?|"
    r"mcp|model context protocol|a2a|agent2agent|agentic|"
    r"agent[- ](?:framework|skills?|harness|memory|orchestration|coding|research|browser|"
    r"platform|runtime|workspace|workbench|development|ide|sdk|cli|os|tools?)|"
    r"(?:coding|research|browser|computer[- ]use|voice|autonomous|multi|parallel)[- ]agents?|"
    r"fleet of parallel agents|ai[- ](?:penetration[- ]testing|pentest)|"
    r"ai[- ](?:agents?|assistant|chat|chatbot|coding|workflow|application|applications|app|"
    r"image|video|voice|search|gateway|observability|productivity|capabilities|powered|driven|"
    r"generated|native|harness|team)|"
    r"prompt[- ](?:engineering|management|optimization)|vector[- ]search|embeddings?|"
    r"model[- ](?:context protocol|serving|inference|fine[- ]tuning)"
    r")\b",
    re.IGNORECASE,
)


def format_month_year(date_str: str) -> str:
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d").replace(tzinfo=UTC)
    except ValueError:
        return ""
    return dt.strftime("[%b %Y]")


def clean_description(text: str, max_len: int = 220) -> str:
    description = " ".join((text or "").replace("\u2728", "").strip().split())
    if not description:
        return ""

    for punct in (".", "!", "?"):
        idx = description.find(punct)
        if 20 <= idx <= max_len:
            return description[: idx + 1]

    if len(description) <= max_len:
        return description

    clipped = description[:max_len].rsplit(" ", 1)[0].rstrip(",;:")
    return f"{clipped} ..."


def build_headers(token: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": DEFAULT_USER_AGENT,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def github_get_json(
    session,
    url: str,
    *,
    headers: dict[str, str],
    params: dict[str, Any],
    timeout: int,
    max_retries: int,
    backoff: float,
) -> dict[str, Any] | None:
    current_backoff = backoff

    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=headers, params=params, timeout=timeout)
        except requests.RequestException:
            if attempt == max_retries - 1:
                return None
            time.sleep(current_backoff)
            current_backoff = min(current_backoff * 2, 60)
            continue

        if response.status_code == 403:
            reset_ts = int(response.headers.get("X-RateLimit-Reset", "0") or 0)
            if reset_ts:
                wait = max(reset_ts - int(time.time()), 0) + 5
                print(f"  [rate-limited] sleeping {wait}s ...")
                time.sleep(wait)
                continue

        if response.status_code == 422:
            return {"items": [], "total_count": 0}

        if response.status_code == 200:
            return response.json()

        if attempt == max_retries - 1:
            return None

        time.sleep(current_backoff)
        current_backoff = min(current_backoff * 2, 60)

    return None


def search_repositories(
    session,
    *,
    query: str,
    query_label: str,
    headers: dict[str, str],
    timeout: int,
    max_retries: int,
    backoff: float,
    sleep_s: float,
    max_pages: int,
) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []

    for page in range(1, max_pages + 1):
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": RESULTS_PER_PAGE,
            "page": page,
        }
        data = github_get_json(
            session,
            GITHUB_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=timeout,
            max_retries=max_retries,
            backoff=backoff,
        )
        if data is None:
            print(f"  [warn] failed query={query_label!r} page={page}")
            break

        items = data.get("items", [])
        if not items:
            break

        repos.extend(items)
        total_count = data.get("total_count", 0)
        fetched_so_far = (page - 1) * RESULTS_PER_PAGE + len(items)
        print(f"  query={query_label!r} page={page} fetched={fetched_so_far}/{total_count}")

        if fetched_so_far >= total_count or len(items) < RESULTS_PER_PAGE:
            break

        time.sleep(sleep_s)

    return repos


def normalize_repo(raw: dict[str, Any]) -> dict[str, Any]:
    owner = raw.get("owner") or {}
    return {
        "name": raw.get("name", ""),
        "full_name": raw.get("full_name", ""),
        "url": raw.get("html_url", ""),
        "description": clean_description(raw.get("description") or ""),
        "stars": raw.get("stargazers_count", 0),
        "forks": raw.get("forks_count", 0),
        "language": raw.get("language") or "",
        "topics": raw.get("topics", []),
        "license": (raw.get("license") or {}).get("spdx_id", ""),
        "created_at": raw.get("created_at", "")[:10],
        "updated_at": raw.get("updated_at", "")[:10],
        "archived": raw.get("archived", False),
        "owner": owner.get("login", ""),
        "owner_type": owner.get("type", ""),
    }


def is_relevant_repo(repo: dict[str, Any]) -> bool:
    """Return whether repository metadata explicitly targets AI/LLM tooling."""
    name_and_topics = " ".join(
        str(value)
        for value in (
            repo.get("name", ""),
            repo.get("full_name", ""),
            " ".join(repo.get("topics", [])),
        )
        if value
    )
    description = str(repo.get("description", ""))
    if re.search(r"\bfor humans and ai agents\b", description, re.IGNORECASE):
        return False
    if re.search(r"\buser agent\b", description, re.IGNORECASE):
        return False

    searchable = " ".join((name_and_topics, description))
    if RELEVANCE_PATTERN.search(searchable):
        return True

    if re.search(r"\bai\b", name_and_topics, re.IGNORECASE):
        return True
    if re.search(r"\bagents?\b", name_and_topics, re.IGNORECASE):
        return True

    # Short descriptions often use AI as the product's entire positioning
    # (for example, "The AI that really does things") rather than a keyword.
    if (
        re.search(r"\bai\b", description, re.IGNORECASE)
        and len(description) <= 45
        and len(description.split()) <= 8
    ):
        return True

    ai_context = re.compile(
        r"\bai\b.{0,16}\b(?:agent|assistant|chat|capabilit\w*|application|app|"
        r"model|workflow|tool|platform|engine|powered|driven|coding|image|video|team|"
        r"turns|creates|generates|builds|writes|produces|transforms|summarizes|summarises|"
        r"voice|search|gateway|observability|productivity|memory|skill|inference|generation|"
        r"generated|summary|summarization|music|audio|speech|translation|presentation|resume|"
        r"design|animation|creation)\w*\b|"
        r"\b(?:agent|assistant|chat|application|app|model|workflow|tool|platform|engine|"
        r"coding|image|video|voice|search|gateway|observability|productivity|memory|skill|"
        r"inference|generation|generated|summary|summarization|music|audio|speech|translation|"
        r"presentation|resume|design|animation|creation)\w*.{0,16}\bai\b|"
        r"\b(?:built|designed|made) for agents\b|"
        r"\b(?:assistant|chatbot|application|app|tool)\b.{0,40}\bai\b|\bfor your ai\b",
        re.IGNORECASE,
    )
    return bool(ai_context.search(description))


def format_compact_entry(repo: dict[str, Any], rank: int) -> str:
    title = repo.get("full_name") or repo.get("name") or "unknown"
    entry = f"{rank}. [{title}]({repo.get('url', '#')})"

    description = repo.get("description", "")
    if description:
        entry += f": {description}"

    date_str = format_month_year(repo.get("created_at", ""))
    if date_str:
        entry += f" {date_str}"

    entry += f" (⭐ {repo.get('stars', 0):,})"
    return entry


def print_table(rows: list[dict[str, Any]], limit: int) -> None:
    print(f"\n{'RANK':<5} {'STARS':>8}  {'FULL NAME':<40}  {'CREATED':<10}  DESCRIPTION")
    print("-" * 130)
    for index, row in enumerate(rows[:limit], 1):
        desc = row.get("description", "")[:60]
        print(
            f"{index:<5} {row.get('stars', 0):>8}  {row.get('full_name', ''):<40}  "
            f"{row.get('created_at', ''):<10}  {desc}"
        )
    if len(rows) > limit:
        print(f"  ... and {len(rows) - limit} more rows")


def save_markdown(
    rows: list[dict[str, Any]],
    path: Path,
    *,
    min_stars: int,
    topics: list[str],
    search_terms: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [format_compact_entry(repo, rank=index) for index, repo in enumerate(rows, 1)]
    with path.open("w", encoding="utf-8") as handle:
        handle.write(f"# Popular LLM Applications (GitHub Stars >= {min_stars})\n\n")
        handle.write(f"*Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}*<br>\n")
        handle.write("*Source: GitHub Search API - deduplicated and relevance-filtered across topic and phrase queries*<br>\n")
        handle.write(f"*Topics searched: {', '.join(topics)}*<br>\n")
        handle.write(f"*Phrases searched in repository name, description, and README: {', '.join(search_terms)}*<br>\n")
        handle.write(f"*Total repositories: {len(rows)}*\n\n")

        if rows:
            handle.write("\n".join(lines) + "\n")
        else:
            handle.write("*No repositories found meeting the criteria.*\n")

    print(f"[saved] Markdown -> {path}")


def parse_markdown_entries(path: Path) -> list[dict[str, Any]]:
    """Parse an existing x_llm_apps.md and return repo dicts."""
    repos: list[dict[str, Any]] = []
    if not path.exists():
        return repos

    pattern = re.compile(
        r'^\d+\.\s+\[([^\]]+?)(?:\u2728)?\]\(([^)]+)\)'
        r'(?::\s*(.*?))?'
        r'\s*(?:\[(\w+ \d{4})\])?'
        r'\s*\(⭐\s*([\d,]+)\)',
        re.MULTILINE,
    )

    text = path.read_text(encoding="utf-8")
    for m in pattern.finditer(text):
        full_name = m.group(1)
        url = m.group(2)
        description = re.sub(r'\s*\[\w+ \d{4}\]$', '', (m.group(3) or "")).strip()
        created_month_year = m.group(4) or ""
        stars = int(m.group(5).replace(",", ""))

        created_at = ""
        if created_month_year:
            try:
                created_at = datetime.strptime(created_month_year, "%b %Y").replace(tzinfo=UTC).strftime("%Y-%m-01")
            except ValueError:
                pass

        parts = full_name.split("/", 1)
        repos.append({
            "name": parts[-1],
            "full_name": full_name,
            "url": url,
            "description": description,
            "stars": stars,
            "forks": 0,
            "language": "",
            "topics": [],
            "license": "",
            "created_at": created_at,
            "updated_at": "",
            "archived": False,
            "owner": parts[0] if len(parts) == 2 else "",
            "owner_type": "",
        })

    return repos


def parse_markdown_topics(path: Path) -> list[str]:
    """Return the topic list recorded in an existing Markdown catalog."""
    if not path.exists():
        return []

    match = re.search(
        r"^\*Topics searched:\s*(.*?)\*(?:<br>)?\s*$",
        path.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if not match:
        return []
    return [topic.strip() for topic in match.group(1).split(",") if topic.strip()]


def parse_markdown_search_terms(path: Path) -> list[str]:
    """Return the phrase-search list recorded in an existing Markdown catalog."""
    if not path.exists():
        return []

    match = re.search(
        r"^\*Phrases searched in repository name, description, and README:\s*(.*?)\*(?:<br>)?\s*$",
        path.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if not match:
        return []
    return [term.strip() for term in match.group(1).split(",") if term.strip()]


def build_search_queries(
    topics: list[str], search_terms: list[str], min_stars: int
) -> list[tuple[str, str]]:
    """Build GitHub searches from tags and phrase-based coverage facets."""
    queries = [
        (f"topic:{topic}", f"topic:{topic} stars:>={min_stars}")
        for topic in topics
    ]
    queries.extend(
        (
            f'phrase:"{term}"',
            f'"{term.replace(chr(34), " ").strip()}" in:name,description,readme stars:>={min_stars}',
        )
        for term in search_terms
    )
    return queries


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch popular GitHub repositories for LLM applications and write a ranked list."
    )
    parser.add_argument(
        "--token",
        default=os.getenv("GITHUB_TOKEN"),
        help="GitHub personal access token. Defaults to GITHUB_TOKEN if set.",
    )
    parser.add_argument(
        "--min-stars",
        type=int,
        default=1000,
        dest="min_stars",
        help="Minimum star count filter (default: 1000).",
    )
    parser.add_argument(
        "--topics",
        nargs="+",
        default=DEFAULT_TOPICS,
        help="GitHub topic tags to search.",
    )
    parser.add_argument(
        "--search-terms",
        nargs="+",
        default=DEFAULT_SEARCH_TERMS,
        help="Phrase searches across repository names, descriptions, and READMEs.",
    )
    parser.add_argument(
        "--output",
        help="Output path. Defaults to section/x_llm_apps.md. Extension controls format: .md, .json, .csv.",
    )
    parser.add_argument(
        "--show",
        type=int,
        default=30,
        help="Number of rows to print to console (default: 30).",
    )
    parser.add_argument("--timeout", type=int, default=20, help="Request timeout in seconds.")
    parser.add_argument("--max-retries", type=int, default=4, help="Max retries per request.")
    parser.add_argument("--backoff", type=float, default=1.0, help="Initial retry backoff in seconds.")
    parser.add_argument("--sleep", type=float, default=1.0, help="Sleep between successful page requests.")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=MAX_PAGES_PER_QUERY,
        help=f"Maximum pages to retrieve per search query (default: {MAX_PAGES_PER_QUERY}).",
    )
    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Include archived repositories. By default archived repos are excluded.",
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Merge results from --topics into existing output, refresh matching entries, then resort by stars.",
    )
    return parser


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    args = build_parser().parse_args()

    root = get_repo_root(__file__)
    output_path = Path(args.output) if args.output else root / "section" / "x_llm_apps.md"
    session = create_session(DEFAULT_USER_AGENT)
    headers = build_headers(args.token)

    if args.token:
        print("[auth] Using token (authenticated GitHub API)")
    else:
        print("[auth] No token - unauthenticated requests are rate-limited")

    print(
        f"[config] topics={len(args.topics)} phrases={len(args.search_terms)} "
        f"min_stars>={args.min_stars} output={output_path}"
    )

    seen: set[str] = set()
    rejected_repos: set[str] = set()
    repos: list[dict[str, Any]] = []
    repo_indices: dict[str, int] = {}
    recorded_topics: list[str] = []
    recorded_search_terms: list[str] = []

    if args.append and output_path.exists():
        print(f"[append] Parsing existing entries from {output_path}")
        existing = parse_markdown_entries(output_path)
        recorded_topics = parse_markdown_topics(output_path)
        recorded_search_terms = parse_markdown_search_terms(output_path)
        print(f"[append] Loaded {len(existing)} existing repositories")
        for repo in existing:
            full_name = repo.get("full_name", "")
            key = full_name.casefold()
            if full_name and not is_relevant_repo(repo):
                rejected_repos.add(key)
                continue
            if full_name and key not in seen:
                seen.add(key)
                repo_indices[key] = len(repos)
                repos.append(repo)

    for query_label, query in build_search_queries(args.topics, args.search_terms, args.min_stars):
        print(f"[search] {query_label}")
        raw_items = search_repositories(
            session,
            query=query,
            query_label=query_label,
            headers=headers,
            timeout=args.timeout,
            max_retries=args.max_retries,
            backoff=args.backoff,
            sleep_s=args.sleep,
            max_pages=args.max_pages,
        )

        added = 0
        for item in raw_items:
            full_name = item.get("full_name", "")
            if not full_name:
                continue

            normalized = normalize_repo(item)
            key = full_name.casefold()
            if not is_relevant_repo(normalized):
                rejected_repos.add(key)
                continue
            rejected_repos.discard(key)
            if normalized["archived"] and not args.include_archived:
                continue

            if key in seen:
                repos[repo_indices[key]] = normalized
            else:
                seen.add(key)
                repo_indices[key] = len(repos)
                repos.append(normalized)
                added += 1

        print(f"  -> {added} new unique repositories (total: {len(repos)})")
        time.sleep(args.sleep)

    if rejected_repos:
        print(f"[filter] excluded {len(rejected_repos)} repositories without clear AI/LLM relevance")

    repos.sort(key=lambda repo: (repo.get("stars", 0), repo.get("full_name", "")), reverse=True)

    print(f"\n[result] {len(repos)} repositories after dedupe and filtering")
    print_table(repos, limit=args.show)

    topics = list(dict.fromkeys([*recorded_topics, *args.topics]))
    search_terms = list(dict.fromkeys([*recorded_search_terms, *args.search_terms]))
    save_markdown(
        repos,
        output_path,
        min_stars=args.min_stars,
        topics=topics,
        search_terms=search_terms,
    )


if __name__ == "__main__":
    main()
