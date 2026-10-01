"""Outbox processor: applies publish side effects recoverably.

Catalog writes insert an `outbox` row in the same transaction as the data change, so a publish
can never be lost between the database and derived systems. This processor handles each row at
least once (handlers are idempotent) and records failures for retry.

Handlers today:
  * catalog.*        -> refresh derived statistics; optionally purge a CDN (CDN_PURGE_URL)
The search index is PostgreSQL itself (generated tsvector + trigram indexes), so it is updated in
the same transaction and cannot drift. If a dedicated search engine is added later, its indexing
handler belongs here.
"""
from __future__ import annotations

import json
import os
import urllib.request

import psycopg
from psycopg.rows import dict_row, tuple_row

MAX_ATTEMPTS = 10


def _purge_cdn(payload: dict) -> None:
    url = os.environ.get("CDN_PURGE_URL")
    if not url:
        return
    req = urllib.request.Request(url, data=json.dumps({"reason": payload}).encode(), method="POST",
                                 headers={"content-type": "application/json",
                                          "authorization": f"Bearer {os.environ.get('CDN_PURGE_TOKEN', '')}"})
    with urllib.request.urlopen(req, timeout=15) as resp:  # noqa: S310 - operator-configured URL
        if resp.status >= 300:
            raise RuntimeError(f"CDN purge failed with HTTP {resp.status}")


def _refresh_stats(conn) -> None:
    from typeicon_import.db import compute_stats
    with conn.cursor(row_factory=tuple_row) as cur:
        stats = compute_stats(cur)
        cur.execute("""INSERT INTO catalog_stats (id, data, computed_at) VALUES ('current', %s, now())
                       ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data, computed_at = now()""",
                    (json.dumps(stats),))


HANDLERS = {
    "catalog.published": [_refresh_stats, _purge_cdn],
    "catalog.design_updated": [_refresh_stats, _purge_cdn],
    "catalog.pack_review": [_refresh_stats, _purge_cdn],
}


def process_outbox(database_url: str, batch: int = 50) -> dict:
    done = failed = 0
    with psycopg.connect(database_url, row_factory=dict_row) as conn:
        rows = conn.execute(
            """SELECT id, topic, payload FROM outbox WHERE processed_at IS NULL AND attempts < %s
               ORDER BY id LIMIT %s FOR UPDATE SKIP LOCKED""", (MAX_ATTEMPTS, batch)).fetchall()
        for row in rows:
            try:
                for handler in HANDLERS.get(row["topic"], []):
                    if handler is _refresh_stats:
                        handler(conn)
                    else:
                        handler(row["payload"])
                conn.execute("UPDATE outbox SET processed_at = now(), attempts = attempts + 1, last_error = NULL WHERE id = %s", (row["id"],))
                done += 1
            except Exception as e:  # noqa: BLE001 - record and retry later
                conn.execute("UPDATE outbox SET attempts = attempts + 1, last_error = %s WHERE id = %s", (str(e)[:500], row["id"]))
                failed += 1
        conn.commit()
    return {"processed": done, "failed": failed}
