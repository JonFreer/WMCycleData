import datetime
from typing import List, Tuple

from sqlalchemy import bindparam, text
from sqlalchemy.orm import Session

from . import models, schemas


def read_counters(db: Session, limit_offset: Tuple[int, int]) -> List[models.Counter]:
    limit, offset = limit_offset
    counters = db.query(models.Counter).offset(offset).limit(limit).all()
    return counters


def read_counters_plus(
    db: Session, limit_offset: Tuple[int, int]
) -> List[schemas.CounterPlus]:
    limit, offset = limit_offset
    counters = (
        db.query(
            models.Counter.identity,
            models.Counter.name,
            models.Counter.lat,
            models.Counter.lon,
            models.Counter.location_desc,
            models.CounterSummary.today_count,
            models.CounterSummary.yesterday_count,
            models.CounterSummary.this_week_count,
            models.CounterSummary.last_week_count,
        )
        .join(
            models.CounterSummary,
            models.Counter.identity == models.CounterSummary.identity,
            isouter=True,
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    return counters


def create_counter(
    db: Session, identity: int, name: str, lat: float, lon: float, location_desc: str
) -> models.Counter:
    counter = (
        db.query(models.Counter).where(models.Counter.identity == identity).first()
    )

    if counter:
        print("Updating Counter")
        counter.name = name
        counter.lat = lat
        counter.lon = lon
        counter.location_desc = location_desc
    else:
        print("Creating Counter")
        counter = models.Counter(
            identity=identity, name=name, lat=lat, lon=lon, location_desc=location_desc
        )
        db.add(counter)

    db.commit()
    db.refresh(counter)
    return counter


def create_counter_summary(
    db: Session,
    identity: int,
    today: int,
    yesterday: int,
    this_week: int,
    last_week: int,
) -> models.CounterSummary:
    counter_summary = (
        db.query(models.CounterSummary)
        .where(models.CounterSummary.identity == identity)
        .first()
    )

    if counter_summary:
        print("Updating Counter")
        counter_summary.today_count = today
        counter_summary.yesterday_count = yesterday
        counter_summary.this_week_count = this_week
        counter_summary.last_week_count = last_week
    else:
        print("Creating Counter")
        counter_summary = models.CounterSummary(
            identity=identity,
            today_count=today,
            yesterday_count=yesterday,
            this_week_count=this_week,
            last_week_count=last_week,
        )
        db.add(counter_summary)

    db.commit()
    db.refresh(counter_summary)
    return counter_summary


def add_count(
    db: Session, counter: str, count_in: int, count_out: int
) -> models.Counts:
    # Validate if the counter is valid
    res = db.query(models.Counter).where(models.Counter.name == counter).all()
    if len(res) == 0:
        raise Exception("Counter name not valid: name not in counters table.")

    db_submission = models.Counts(
        timestamp=datetime.datetime.now(),
        count_in=count_in,
        count_out=count_out,
        counter=counter,
    )

    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)

    return db_submission


def add_count_time(
    db: Session,
    counter_identity: int,
    count_in: int,
    count_out: int,
    time: datetime.datetime,
    mode: str,
) -> models.Counts:
    # # Validate if the counter is valid
    # res = (
    #     db.query(models.Counter)
    #     .where(models.Counter.identity == counter_identity)
    #     .all()
    # )
    # if len(res) == 0:
    #     raise Exception("Counter name not valid: name not in counters table.")

    # Check if key is in db
    query = (
        db.query(models.Counts)
        .where(models.Counts.counter == counter_identity)
        .where(models.Counts.timestamp == time)
        .where(models.Counts.mode == mode)
    )

    db_submission = query.first()

    if db_submission:  # If value in db update
        db_submission.count_in = count_in
        db_submission.count_out = count_out
        print("updating")
    else:  # If value not in db, add it to the db
        db_submission = models.Counts(
            timestamp=time,
            mode=mode,
            count_in=count_in,
            count_out=count_out,
            counter=counter_identity,
        )
        db.add(db_submission)

    db.commit()
    db.refresh(db_submission)

    return db_submission


def read_all_counts(
    db: Session, limit_offset: Tuple[int, int], time_interval: str
) -> List[models.Counts]:
    limit, offset = limit_offset
    # counters = db.query(models.Counts).offset(offset).limit(limit).all()
    sql = text(
        """SELECT time_bucket(:timeInterval, timestamp) as timestamp, 
               mode, counter ,
               sum(count_in) as count_in, 
               sum(count_out) as count_out 
               
               from counts 
               GROUP BY 1,2,3
               ORDER BY timestamp DESC"""
    )
    sql = sql.bindparams(
        bindparam("timeInterval", value=time_interval))
    results = db.execute(sql).all()
    print(results)
    return results


def read_counts(
    db: Session,
    limit_offset: Tuple[int, int],
    time_interval: str,
    identity: int,
    start_time: int,
    table: str = "counts_hourly",
) -> List[models.Counts]:
    limit, offset = limit_offset

    sql = text(
        """SELECT time_bucket(:timeInterval , timestamp) as timestamp, 
               mode, counter ,
               sum(count_in) as count_in, 
               sum(count_out) as count_out 
               FROM """
        + table
        + """ 
               WHERE counter = :identity AND timestamp > TIMESTAMPTZ :start_time
               GROUP BY 1,2,3
               ORDER BY timestamp DESC"""
    )

    sql = sql.bindparams(
        bindparam("timeInterval", value=time_interval),
        bindparam("identity", value=identity),
        bindparam("start_time", value=datetime.datetime.fromtimestamp(start_time)),
    )

    results = db.execute(sql).all()
    return results
