"""Monthly response caching and cross-process pacing for paper update scripts."""

from __future__ import annotations

import json
import random
import sqlite3
import time
from contextlib import closing
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any

import requests


class RateLimitDeferred(RuntimeError):
    """A throttled discovery query must be resumed in a later run."""


class SemanticScholarSession(requests.Session):
    def __init__(
        self,
        cache_dir: Path,
        *,
        request_delay: float,
        jitter: float,
        user_agent: str | None = None,
    ) -> None:
        super().__init__()
        if user_agent:
            self.headers.update({"User-Agent": user_agent})
        self.request_delay = max(request_delay, 1.0)
        self.jitter = max(jitter, 0.0)
        cache_dir.mkdir(parents=True, exist_ok=True)
        ignore_file = cache_dir / ".gitignore"
        if not ignore_file.exists():
            ignore_file.write_text("*\n", encoding="utf-8")
        self.database = cache_dir / "requests.sqlite3"
        with closing(sqlite3.connect(self.database, timeout=1800)) as connection, connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS responses "
                "(period TEXT, key TEXT, payload TEXT NOT NULL, PRIMARY KEY (period, key))"
            )
            connection.execute(
                "CREATE TABLE IF NOT EXISTS pacing "
                "(id INTEGER PRIMARY KEY CHECK (id = 1), next_request REAL NOT NULL, failures INTEGER NOT NULL)"
            )
            connection.execute("INSERT OR IGNORE INTO pacing VALUES (1, 0, 0)")

    @staticmethod
    def _response(url: str, payload: Any) -> requests.Response:
        response = requests.Response()
        response.status_code = 200
        response.url = url
        response.encoding = "utf-8"
        response.headers["Content-Type"] = "application/json"
        response._content = json.dumps(payload).encode("utf-8")
        return response

    @staticmethod
    def _key(url: str, params: dict, identifier: str | None = None) -> str:
        normalized = dict(params)
        if "fields" in normalized:
            normalized["fields"] = ",".join(sorted(normalized["fields"].split(",")))
        return json.dumps([url, normalized, identifier], sort_keys=True)

    @staticmethod
    def _retry_after(value: str | None) -> float:
        if not value:
            return 0.0
        try:
            return max(float(value), 0.0)
        except ValueError:
            try:
                return max(parsedate_to_datetime(value).timestamp() - time.time(), 0.0)
            except (ValueError, TypeError, OverflowError):
                print(f"  [WARN] Invalid Semantic Scholar Retry-After header: {value!r}")
                return 0.0

    def _store_paper(
        self, connection: sqlite3.Connection, period: str, paper: dict, fields: str, identifier: str | None = None,
    ) -> None:
        identifiers = {identifier, paper.get("paperId")}
        arxiv_id = (paper.get("externalIds") or {}).get("ArXiv")
        if arxiv_id:
            identifiers.add(f"ARXIV:{arxiv_id}")
        batch_url = "https://api.semanticscholar.org/graph/v1/paper/batch"
        for lookup_id in identifiers - {None}:
            key = self._key(batch_url, {"fields": fields}, lookup_id)
            connection.execute(
                "INSERT OR REPLACE INTO responses VALUES (?, ?, ?)",
                (period, key, json.dumps(paper)),
            )
            if isinstance(paper.get("citationCount"), int):
                key = self._key(batch_url, {"fields": "citationCount"}, lookup_id)
                connection.execute(
                    "INSERT OR REPLACE INTO responses VALUES (?, ?, ?)",
                    (period, key, json.dumps({
                        "paperId": paper.get("paperId"), "citationCount": paper["citationCount"],
                    })),
                )

    def cached_papers(self, ids: list[str], fields: list[str]) -> dict[str, dict]:
        """Return successful batch records from the current month's cache without making requests."""
        period = datetime.now(UTC).strftime("%Y-%m")
        url = "https://api.semanticscholar.org/graph/v1/paper/batch"
        params = {"fields": ",".join(fields)}
        cached: dict[str, dict] = {}
        with closing(sqlite3.connect(self.database, timeout=1800)) as connection:
            for identifier in dict.fromkeys(ids):
                row = connection.execute(
                    "SELECT payload FROM responses WHERE period = ? AND key = ?",
                    (period, self._key(url, params, identifier)),
                ).fetchone()
                if row:
                    cached[identifier] = json.loads(row[0])
        return cached

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        params = kwargs.get("params") or {}
        period = datetime.now(UTC).strftime("%Y-%m")
        batch = method.upper() == "POST" and url.endswith("/paper/batch")
        ids = kwargs["json"]["ids"] if batch else []
        key = self._key(url, params)
        with closing(sqlite3.connect(self.database, timeout=1800)) as connection:
            # Hold the transaction through the request so separate scripts cannot
            # overlap HTTP requests or bypass a cooldown recorded by another process.
            connection.execute("BEGIN IMMEDIATE")
            try:
                cached: dict[str, dict] = {}
                if batch:
                    for identifier in ids:
                        row = connection.execute(
                            "SELECT payload FROM responses WHERE period = ? AND key = ?",
                            (period, self._key(url, params, identifier)),
                        ).fetchone()
                        if row:
                            cached[identifier] = json.loads(row[0])
                    pending = list(dict.fromkeys(identifier for identifier in ids if identifier not in cached))
                    if not pending:
                        print(f"  [cache] {len(ids)} paper(s) from {period}")
                        return self._response(url, [cached[identifier] for identifier in ids])
                    kwargs["json"] = {**kwargs["json"], "ids": pending}
                    if cached:
                        print(f"  [cache] {len(cached)} paper(s); requesting {len(pending)} outstanding ID(s)")
                else:
                    row = connection.execute(
                        "SELECT payload FROM responses WHERE period = ? AND key = ?", (period, key),
                    ).fetchone()
                    if row:
                        print(f"  [cache] {params.get('query', url)} ({period})")
                        return self._response(url, json.loads(row[0]))

                next_request, failures = connection.execute(
                    "SELECT next_request, failures FROM pacing WHERE id = 1"
                ).fetchone()
                wait = next_request - time.time()
                if wait > 0:
                    print(f"  [pace] Waiting {wait:.1f}s for shared Semantic Scholar request slot")
                    time.sleep(wait)
                try:
                    response = super().request(method, url, **kwargs)
                finally:
                    connection.execute(
                        "UPDATE pacing SET next_request = ? WHERE id = 1",
                        (time.time() + self.request_delay + random.uniform(0, self.jitter),),
                    )

                if response.status_code == 429:
                    cooldown = max(min(120.0 * 2 ** min(failures, 3), 900.0),
                                   self._retry_after(response.headers.get("Retry-After")))
                    connection.execute(
                        "UPDATE pacing SET next_request = ?, failures = ? WHERE id = 1",
                        (time.time() + max(cooldown, self.request_delay), failures + 1),
                    )
                    print(f"  [429] Shared cooldown {cooldown:.0f}s; failed request remains pending")
                elif response.status_code == 200:
                    payload = response.json()
                    if batch:
                        if not isinstance(payload, list) or len(payload) != len(pending):
                            raise ValueError("Semantic Scholar batch response does not match the requested IDs")
                        if any(paper is not None and not isinstance(paper, dict) for paper in payload):
                            raise ValueError("Semantic Scholar batch response contains an invalid paper")
                        if "citationCount" in params["fields"].split(",") and any(
                            paper is not None and (
                                not isinstance(paper.get("citationCount"), int) or paper["citationCount"] < 0
                            ) for paper in payload
                        ):
                            raise ValueError("Semantic Scholar batch response contains an invalid citation count")
                        for identifier, paper in zip(pending, payload):
                            if paper:
                                self._store_paper(connection, period, paper, params["fields"], identifier)
                        fetched = dict(zip(pending, payload))
                        response = self._response(url, [
                            cached[identifier] if identifier in cached else fetched[identifier]
                            for identifier in ids
                        ])
                    elif url.endswith(("/paper/search", "/paper/search/bulk")):
                        if (
                            not isinstance(payload, dict) or not isinstance(payload.get("data"), list)
                            or any(not isinstance(paper, dict) for paper in payload["data"])
                        ):
                            raise ValueError("Semantic Scholar search response is missing its data list")
                        connection.execute(
                            "INSERT OR REPLACE INTO responses VALUES (?, ?, ?)", (period, key, json.dumps(payload)),
                        )
                        for paper in payload["data"]:
                            self._store_paper(connection, period, paper, params["fields"])
                    else:
                        if not isinstance(payload, dict) or not payload.get("paperId"):
                            raise ValueError("Semantic Scholar response is missing its paper ID")
                        connection.execute(
                            "INSERT OR REPLACE INTO responses VALUES (?, ?, ?)", (period, key, json.dumps(payload)),
                        )
                        self._store_paper(connection, period, payload, params["fields"])
                    connection.execute("UPDATE pacing SET failures = 0 WHERE id = 1")
                return response
            finally:
                connection.commit()
