"""PostgreSQL-backed durable job queue.

Claiming uses `FOR UPDATE SKIP LOCKED`, so any number of workers can poll the same table
without double-processing. Running jobs send heartbeats; a job whose heartbeat stops (crash,
OOM kill, lost host) is re-queued by `recover_stale` until max_attempts, then failed.
Failures are retried with exponential backoff unless marked permanent.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb


@dataclass
class Job:
    id: str
    kind: str
    payload: dict
    scope: str
    owner_id: str | None
    cache_key: str | None
    attempts: int
    max_attempts: int


class PermanentError(RuntimeError):
    """A failure that retrying cannot fix (invalid input, missing asset)."""


class JobQueue:
    def __init__(self, database_url: str, worker_id: str):
        self.url = database_url
        self.worker_id = worker_id

    def _conn(self):
        return psycopg.connect(self.url, autocommit=True, row_factory=dict_row)

    def claim(self, kinds: list[str] | None = None) -> Job | None:
        kinds = kinds or ["custom_icon_check", "subset_build", "kit_build", "catalog_import", "release_build"]
        with self._conn() as c:
            row = c.execute(
                """UPDATE jobs SET status = 'running', locked_by = %s, locked_at = now(), heartbeat_at = now(),
                          started_at = coalesce(started_at, now()), attempts = attempts + 1
                   WHERE id = (SELECT id FROM jobs WHERE status = 'queued' AND run_after <= now() AND kind = ANY(%s)
                               ORDER BY created_at FOR UPDATE SKIP LOCKED LIMIT 1)
                   RETURNING id, kind, payload, scope, owner_id, cache_key, attempts, max_attempts""",
                (self.worker_id, kinds),
            ).fetchone()
        if not row:
            return None
        return Job(id=str(row["id"]), kind=row["kind"], payload=row["payload"], scope=row["scope"],
                   owner_id=row["owner_id"], cache_key=row["cache_key"], attempts=row["attempts"],
                   max_attempts=row["max_attempts"])

    def heartbeat(self, job_id: str) -> None:
        with self._conn() as c:
            c.execute("UPDATE jobs SET heartbeat_at = now() WHERE id = %s AND locked_by = %s", (job_id, self.worker_id))

    def succeed(self, job: Job, result: dict) -> None:
        with self._conn() as c:
            c.execute("""UPDATE jobs SET status = 'succeeded', result = %s, error = NULL, finished_at = now(),
                                locked_by = NULL WHERE id = %s""", (Jsonb(result), job.id))
            c.execute("""INSERT INTO audit_events (actor_id, action, subject_type, subject_id, data)
                         VALUES (%s, 'build.succeeded', 'job', %s, %s)""",
                      (f"system:{self.worker_id}", job.id, Jsonb({"kind": job.kind, "attempts": job.attempts})))

    def fail(self, job: Job, error: str, permanent: bool = False) -> str:
        error = error[:2000]
        with self._conn() as c:
            if not permanent and job.attempts < job.max_attempts:
                delay = min(600, 10 * 2 ** (job.attempts - 1))
                c.execute("""UPDATE jobs SET status = 'queued', error = %s, locked_by = NULL,
                                    run_after = now() + make_interval(secs => %s) WHERE id = %s""", (error, delay, job.id))
                return "retry"
            c.execute("""UPDATE jobs SET status = 'failed', error = %s, finished_at = now(), locked_by = NULL
                         WHERE id = %s""", (error, job.id))
            c.execute("""INSERT INTO audit_events (actor_id, action, subject_type, subject_id, data)
                         VALUES (%s, 'build.failed', 'job', %s, %s)""",
                      (f"system:{self.worker_id}", job.id, Jsonb({"kind": job.kind, "error": error[:300]})))
            return "failed"

    def recover_stale(self, stale_seconds: int) -> int:
        with self._conn() as c:
            requeued = c.execute(
                """UPDATE jobs SET status = 'queued', locked_by = NULL, run_after = now(),
                          error = 'worker heartbeat lost; re-queued'
                   WHERE status = 'running' AND heartbeat_at < now() - make_interval(secs => %s)
                     AND attempts < max_attempts RETURNING id""", (stale_seconds,)).fetchall()
            c.execute(
                """UPDATE jobs SET status = 'failed', locked_by = NULL, finished_at = now(),
                          error = 'worker heartbeat lost after final attempt'
                   WHERE status = 'running' AND heartbeat_at < now() - make_interval(secs => %s)
                     AND attempts >= max_attempts""", (stale_seconds,))
        return len(requeued)

    def depth(self) -> dict:
        with self._conn() as c:
            rows = c.execute("SELECT status, count(*) AS n FROM jobs GROUP BY status").fetchall()
        return {r["status"]: r["n"] for r in rows}


def dumps(o) -> str:
    return json.dumps(o, separators=(",", ":"), sort_keys=True)
