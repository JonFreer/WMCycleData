"""The Vivacity load, lifted out of the request handler.

Run by the worker in tasks.py, so every function here takes the session it
should use rather than a request scoped one.
"""

import datetime

from sqlalchemy.orm import Session

from . import config, crud, vivacity

DAY_SECONDS = 86400

# What the old hourly_load.sh asked for.
HOURLY_DELTA_T = 4 * 60 * 60

# back_load.sh walked backwards from this timestamp one week per run, asking
# for a slightly wider window than the step so the edges overlap.
BACKFILL_START = 1685947453
BACKFILL_STEP = 604800
BACKFILL_DELTA_T = 704800


def load_vivacity_counts(
    db: Session,
    delta_t: int,
    identity: int | None = None,
    end_t: int | None = None,
) -> dict:
    """Pull counts from Vivacity, store them, then rebuild the summaries."""
    counters = crud.read_counters(db, [None, 0])

    results, counters_vivacity = vivacity.Vivacity.get_counts(
        config.VivacityKey, delta_t, identity, end_t
    )

    # Add any new counters to the counters table
    counters_identitys = map(lambda x: x.identity, counters)
    new_counters = set(counters_vivacity).difference(set(counters_identitys))

    print("counters_identity", new_counters)

    for counter_id in new_counters:
        crud.create_counter(
            db,
            counter_id,
            "",
            counters_vivacity[counter_id].split(",")[0],
            counters_vivacity[counter_id].split(",")[1],
            "",
        )

    for count in results:
        crud.add_count_time(
            db,
            count["identity"],
            count["counts"]["In"],
            count["counts"]["Out"],
            count["timestamp"],
            count["mode"],
        )

    # add_count_time leaves its inserts pending, and with no counters to
    # summarise nothing downstream would commit them.
    db.commit()

    refresh_counter_summaries(db)

    return {"counts": len(results), "new_counters": len(new_counters)}


def refresh_counter_summaries(db: Session) -> None:
    """Recalculate the cached daily and weekly totals for every counter."""
    counters = crud.read_counters(db, (None, 0))

    for counter in counters:
        today = 0
        yesterday = 0
        week_count = 0
        last_week_count = 0

        today_res = crud.read_counts(
            db,
            (None, 0),
            time_interval="1 day",
            identity=counter.identity,
            start_time=int(datetime.datetime.now().timestamp() - DAY_SECONDS * 2),
            table="counts",
        )
        week_res = crud.read_counts(
            db,
            (None, 0),
            time_interval="1 week",
            identity=counter.identity,
            start_time=int(datetime.datetime.now().timestamp() - DAY_SECONDS * 14),
            table="counts",
        )

        today_res = list(filter(lambda x: (x.mode == "cyclist"), today_res))
        week_res = list(filter(lambda x: (x.mode == "cyclist"), week_res))

        if len(today_res) > 0:
            today = today_res[0].count_in + today_res[0].count_out

        if len(today_res) > 1:
            yesterday = today_res[1].count_in + today_res[1].count_out

        if len(week_res) > 0:
            week_count = week_res[0].count_in + week_res[0].count_out

        if len(week_res) > 1:
            last_week_count = week_res[1].count_in + week_res[1].count_out

        crud.create_counter_summary(
            db, counter.identity, today, yesterday, week_count, last_week_count
        )


def hourly_load(db: Session) -> dict:
    """Pick up the last few hours of counts."""
    return load_vivacity_counts(db, delta_t=HOURLY_DELTA_T)


def back_load(db: Session) -> dict:
    """Load one more week of history, working backwards from BACKFILL_START."""
    state = crud.get_job_state(db, "back_load", datetime.datetime.now(datetime.timezone.utc))
    end_t = BACKFILL_START - state.cursor * BACKFILL_STEP

    result = load_vivacity_counts(db, delta_t=BACKFILL_DELTA_T, end_t=end_t)

    # Only move the cursor on a load that got this far, so a failed week is
    # retried rather than skipped.
    state.cursor += 1
    db.commit()

    return {**result, "window_end": end_t, "cursor": state.cursor}
