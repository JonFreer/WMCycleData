"""A single background worker for the long running load jobs.

/load_vivacity/ used to do the Vivacity request, the inserts and the summary
rebuild inside the request itself, which took tens of seconds. Jobs run here
instead, on one worker thread, which also keeps two scheduled loads off the
same rows when their due times land together.
"""

import datetime
import threading
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor

from .db import SessionLocal

# One worker, so loads queue behind each other rather than overlapping.
_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="loader")

_lock = threading.Lock()
_jobs: dict[str, dict] = {}

# Records are only kept so a caller can look up how a load went.
MAX_JOBS = 20


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _update(job_id: str, **fields) -> None:
    with _lock:
        _jobs[job_id].update(fields)


def _prune() -> None:
    finished = [
        job
        for job in sorted(_jobs.values(), key=lambda job: job["queued_at"])
        if job["status"] in ("succeeded", "failed")
    ]
    for job in finished[: max(len(_jobs) - MAX_JOBS, 0)]:
        del _jobs[job["id"]]


def submit(name: str, func, **kwargs) -> dict:
    """Queue func(db, **kwargs) on the worker and return the job record."""
    job = {
        "id": uuid.uuid4().hex,
        "name": name,
        "status": "queued",
        "queued_at": _now(),
        "started_at": None,
        "finished_at": None,
        "detail": None,
    }

    with _lock:
        _jobs[job["id"]] = job
        _prune()

    _executor.submit(_run, job["id"], func, kwargs)
    return dict(job)


def _run(job_id: str, func, kwargs: dict) -> None:
    _update(job_id, status="running", started_at=_now())

    # The request that queued this is long gone, so the job owns its session.
    db = SessionLocal()
    try:
        detail = func(db, **kwargs)
        _update(job_id, status="succeeded", finished_at=_now(), detail=detail)
    except Exception as e:
        traceback.print_exc()
        _update(job_id, status="failed", finished_at=_now(), detail=repr(e))
    finally:
        db.close()


def active(name: str) -> bool:
    """True if a job of this name is queued or still running."""
    with _lock:
        return any(
            job["name"] == name and job["status"] in ("queued", "running")
            for job in _jobs.values()
        )


def get(job_id: str) -> dict | None:
    with _lock:
        job = _jobs.get(job_id)
        return dict(job) if job else None


def recent() -> list[dict]:
    with _lock:
        return [
            dict(job)
            for job in sorted(
                _jobs.values(), key=lambda job: job["queued_at"], reverse=True
            )
        ]
