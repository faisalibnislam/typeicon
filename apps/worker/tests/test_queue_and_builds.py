"""Worker queue semantics and build ownership isolation, against the test database."""
import json
import os
import uuid

import psycopg
import pytest

from typeicon_worker.queue import Job, JobQueue, PermanentError

URL = os.environ.get("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not URL, reason="TEST_DATABASE_URL not set")


@pytest.fixture
def conn():
    with psycopg.connect(URL, autocommit=True) as c:
        c.execute("DELETE FROM jobs WHERE kind LIKE 'test_%'")
        yield c
        c.execute("DELETE FROM jobs WHERE kind LIKE 'test_%'")


def insert(conn, kind="test_job", max_attempts=3, scope="public", owner=None):
    return str(conn.execute("INSERT INTO jobs (kind, payload, max_attempts, scope, owner_id) VALUES (%s, '{}'::jsonb, %s, %s, %s) RETURNING id",
                            (kind, max_attempts, scope, owner)).fetchone()[0])


def test_skip_locked_claims_are_exclusive(conn):
    ids = {insert(conn), insert(conn)}
    q1, q2 = JobQueue(URL, "w1"), JobQueue(URL, "w2")
    a, b = q1.claim(["test_job"]), q2.claim(["test_job"])
    assert a and b and a.id != b.id and {a.id, b.id} == ids
    assert q1.claim(["test_job"]) is None


def test_retry_with_backoff_then_fail(conn):
    insert(conn, max_attempts=2)
    q = JobQueue(URL, "w")
    job = q.claim(["test_job"])
    assert q.fail(job, "boom") == "retry"
    status, run_after_future = conn.execute("SELECT status, run_after > now() FROM jobs WHERE id = %s", (job.id,)).fetchone()
    assert status == "queued" and run_after_future
    conn.execute("UPDATE jobs SET run_after = now() WHERE id = %s", (job.id,))
    job = q.claim(["test_job"])
    assert job.attempts == 2
    assert q.fail(job, "boom again") == "failed"
    assert conn.execute("SELECT status FROM jobs WHERE id = %s", (job.id,)).fetchone()[0] == "failed"


def test_permanent_errors_are_not_retried(conn):
    insert(conn)
    q = JobQueue(URL, "w")
    job = q.claim(["test_job"])
    assert q.fail(job, "bad input", permanent=True) == "failed"


def test_stale_running_jobs_are_recovered(conn):
    jid = insert(conn)
    q = JobQueue(URL, "w")
    q.claim(["test_job"])
    conn.execute("UPDATE jobs SET heartbeat_at = now() - interval '10 minutes' WHERE id = %s", (jid,))
    assert q.recover_stale(60) == 1
    assert conn.execute("SELECT status FROM jobs WHERE id = %s", (jid,)).fetchone()[0] == "queued"


def test_kit_build_refuses_foreign_scope_and_custom_icons():
    from typeicon_worker.kit_build import run_kit_build
    job = Job(id=str(uuid.uuid4()), kind="kit_build", payload={"kitId": str(uuid.uuid4()), "kitVersionId": str(uuid.uuid4()), "version": 1,
              "slug": "x", "release": "0.1.0"}, scope="private:someone-else", owner_id="me", cache_key="0" * 64, attempts=1, max_attempts=1)
    with pytest.raises(PermanentError, match="private scope"):
        run_kit_build(job, URL)


def test_subset_build_refuses_private_scope():
    from typeicon_worker.subset_build import run_subset_build
    job = Job(id=str(uuid.uuid4()), kind="subset_build", payload={"name": "x", "slug": "x", "formats": ["svg"], "release": "0.1.0", "items": []},
              scope="private:me", owner_id="me", cache_key="0" * 64, attempts=1, max_attempts=1)
    with pytest.raises(PermanentError, match="public catalog"):
        run_subset_build(job, URL)
