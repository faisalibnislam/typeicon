"""TypeIcon worker: claims jobs from PostgreSQL and runs them in isolated child processes.

Each job runs in a fresh process with resource limits (CPU seconds, address space where the
OS enforces it) and a wall-clock timeout. The parent sends heartbeats while it waits and kills
the child if it exceeds the timeout. Usage:

  typeicon-worker                 # poll forever
  typeicon-worker --once          # process at most one job (tests, cron)
  typeicon-worker --drain         # process until the queue is empty, then exit
"""
from __future__ import annotations

import argparse
import multiprocessing as mp
import os
import signal
import socket
import sys
import time
import traceback

from .queue import Job, JobQueue, PermanentError

JOB_TIMEOUT = int(os.environ.get("WORKER_JOB_TIMEOUT_SECONDS", "300"))
MEMORY_LIMIT_MB = int(os.environ.get("WORKER_MEMORY_LIMIT_MB", "2048"))
POLL_SECONDS = float(os.environ.get("WORKER_POLL_SECONDS", "1.5"))
HEARTBEAT_SECONDS = 5
STALE_SECONDS = max(60, HEARTBEAT_SECONDS * 6)


# Long-running admin jobs get a larger budget; user-triggered builds stay tightly bounded.
KIND_TIMEOUT = {"release_build": int(os.environ.get("WORKER_RELEASE_TIMEOUT_SECONDS", "3600")),
                "catalog_import": int(os.environ.get("WORKER_IMPORT_TIMEOUT_SECONDS", "1800"))}


def _timeout(kind: str) -> int:
    return KIND_TIMEOUT.get(kind, JOB_TIMEOUT)


def _limits(kind: str = "") -> None:
    import resource
    t = _timeout(kind)
    # Release builds use a process pool, so their CPU budget is per-process, not wall-clock.
    resource.setrlimit(resource.RLIMIT_CPU, (t, t + 5))
    if sys.platform.startswith("linux"):  # macOS does not enforce RLIMIT_AS
        limit = MEMORY_LIMIT_MB * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))


def _child(job: Job, database_url: str, conn) -> None:
    try:
        _limits(job.kind)
        if job.kind == "subset_build":
            from .subset_build import run_subset_build
            result = run_subset_build(job, database_url)
        elif job.kind == "kit_build":
            from .kit_build import run_kit_build
            result = run_kit_build(job, database_url)
        elif job.kind == "catalog_import":
            from .admin_jobs import run_catalog_import
            result = run_catalog_import(job, database_url)
        elif job.kind == "release_build":
            from .admin_jobs import run_release_build
            result = run_release_build(job, database_url)
        elif job.kind == "custom_icon_check":
            from .kit_build import run_custom_icon_check
            result = run_custom_icon_check(job, database_url)
        else:
            raise PermanentError(f"unknown job kind {job.kind}")
        conn.send(("ok", result))
    except PermanentError as e:
        conn.send(("permanent", str(e)))
    except MemoryError:
        conn.send(("error", "out of memory"))
    except Exception as e:  # noqa: BLE001 - report every failure to the queue
        conn.send(("error", f"{type(e).__name__}: {e}\n{traceback.format_exc(limit=5)}"))
    finally:
        conn.close()


def run_job(queue: JobQueue, job: Job, database_url: str, log=print) -> str:
    ctx = mp.get_context("spawn")
    parent, child = ctx.Pipe(duplex=False)
    # Not daemonic: import and release jobs use process pools. The parent kills it on timeout.
    proc = ctx.Process(target=_child, args=(job, database_url, child), daemon=False)
    started = time.monotonic()
    proc.start()
    child.close()
    outcome = None
    while True:
        if parent.poll(HEARTBEAT_SECONDS):
            try:
                outcome = parent.recv()
            except EOFError:
                outcome = None
            break
        queue.heartbeat(job.id)
        if time.monotonic() - started > _timeout(job.kind):
            proc.kill()
            outcome = ("error", f"timed out after {_timeout(job.kind)}s")
            break
        if not proc.is_alive():
            outcome = ("error", f"worker process exited with code {proc.exitcode}")
            break
    proc.join(timeout=10)
    if proc.is_alive():
        proc.kill()
    if outcome is None:
        outcome = ("error", f"worker process exited with code {proc.exitcode} (possibly killed for exceeding limits)")
    kind, value = outcome
    took = time.monotonic() - started
    if kind == "ok":
        queue.succeed(job, value)
        log(f"[worker] job {job.id} {job.kind} succeeded in {took:.1f}s")
        return "succeeded"
    state = queue.fail(job, value, permanent=(kind == "permanent"))
    log(f"[worker] job {job.id} {job.kind} {state}: {value.splitlines()[0][:200]}")
    return state


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="typeicon-worker")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--drain", action="store_true")
    args = ap.parse_args(argv)
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("DATABASE_URL is required", file=sys.stderr)
        return 2
    worker_id = f"{socket.gethostname()}:{os.getpid()}"
    queue = JobQueue(url, worker_id)
    stop = False

    def _stop(*_):
        nonlocal stop
        stop = True
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    print(f"[worker] {worker_id} started (timeout {JOB_TIMEOUT}s, memory {MEMORY_LIMIT_MB} MB)")
    last_recover = 0.0
    while not stop:
        if time.monotonic() - last_recover > 30:
            n = queue.recover_stale(STALE_SECONDS)
            if n:
                print(f"[worker] re-queued {n} stale job(s)")
            from .outbox import process_outbox
            ob = process_outbox(url)
            if ob["processed"] or ob["failed"]:
                print(f"[worker] outbox: {ob}")
            last_recover = time.monotonic()
        job = queue.claim()
        if job is None:
            if args.once or args.drain:
                break
            time.sleep(POLL_SECONDS)
            continue
        run_job(queue, job, url)
        if args.once:
            break
    print("[worker] stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
