"""Runs the scheduled loads in process, in place of the ofelia container.

Due times live in the job_state table rather than in a sleep interval, so a
restart (or a --reload) picks the schedule up where it left off instead of
starting the clock again. The tick is cheap, so it runs often and the table
decides what is actually due.
"""

import dataclasses
import datetime
import threading
import time
import traceback
from typing import Callable

from . import crud, loader, tasks
from .db import SessionLocal

TICK_SECONDS = 60


@dataclasses.dataclass(frozen=True)
class ScheduledJob:
    name: str
    func: Callable
    interval: datetime.timedelta
    # Delay before the first run, so the jobs do not all land together the way
    # the two @every 1h ofelia jobs did.
    offset: datetime.timedelta = datetime.timedelta()


JOBS = [
    ScheduledJob("hourly_load", loader.hourly_load, datetime.timedelta(hours=1)),
    ScheduledJob(
        "back_load",
        loader.back_load,
        datetime.timedelta(hours=1),
        offset=datetime.timedelta(minutes=30),
    ),
]


def tick() -> None:
    now = datetime.datetime.now(datetime.timezone.utc)
    db = SessionLocal()

    try:
        for job in JOBS:
            state = crud.get_job_state(db, job.name, now - job.interval + job.offset)

            if now - state.last_run < job.interval:
                continue

            if tasks.active(job.name):
                # Still working through the last one. Leave it due and look
                # again next tick rather than piling runs up on the worker.
                print(f"scheduler: {job.name} is due but still running")
                continue

            print(f"scheduler: queueing {job.name}")
            tasks.submit(job.name, job.func)
            state.last_run = now
            db.commit()
    finally:
        db.close()


def _loop() -> None:
    while True:
        try:
            tick()
        except Exception:
            # A bad tick must not take the schedule down with it.
            traceback.print_exc()
        time.sleep(TICK_SECONDS)


def start() -> threading.Thread:
    thread = threading.Thread(target=_loop, name="scheduler", daemon=True)
    thread.start()
    return thread
