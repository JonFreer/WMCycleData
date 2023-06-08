from datetime import datetime
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, cast, DateTime, text

from . import config, models
from typing import Any, Dict, List, Optional, Tuple, Union

import datetime


def read_counters(db: Session, limit_offset: Tuple[int, int]) -> List[models.Counter]:
    limit, offset = limit_offset
    counters = db.query(models.Counter).offset(offset).limit(limit).all()
    return counters


def create_counter(db: Session,identity:int, name: str, lat: float, lon: float, location_desc: str) -> models.Counter:
    print("Creating Counter")
    db_submission = models.Counter(
        identity= identity,
        name=name,
        lat=lat,
        lon=lon,
        location_desc=location_desc)

    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def add_count(db: Session, counter: str, count_in: int, count_out: int) -> models.Counts:

    # Validate if the counter is valid
    res = db.query(models.Counter).where(models.Counter.name == counter).all()
    if len(res) == 0:
        raise Exception("Counter name not valid: name not in counters table.")

    db_submission = models.Counts(
        timestamp=datetime.datetime.now(),
        count_in=count_in,
        count_out=count_out,
        counter=counter
    )

    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)

    return db_submission


def add_count_time(db: Session, counter: str, count_in: int, count_out: int, time: datetime.datetime, mode:str) -> models.Counts:
    # Validate if the counter is valid
    res = db.query(models.Counter).where(models.Counter.name == counter).all()
    if len(res) == 0:
        raise Exception("Counter name not valid: name not in counters table.")

    # Check if key is in db
    query = db.query(models.Counts).where(models.Counts.counter == counter) \
        .where(models.Counts.timestamp == time) \
        .where(models.Counts.mode == mode)
    
    db_submission = query.first()

    if db_submission: # If value in db update
        db_submission.count_in = count_in
        db_submission.count_out = count_out
        print("updating")
    else: # If value not in db, add it to the db
        db_submission = models.Counts(
            timestamp=time,
            mode = mode,
            count_in=count_in,
            count_out=count_out,
            counter=counter
        )
        db.add(db_submission)

    db.commit()
    db.refresh(db_submission)

    return db_submission


def read_all_counts(db: Session, limit_offset: Tuple[int, int], time_interval:str) -> List[models.Counts]:
    limit, offset = limit_offset
    # counters = db.query(models.Counts).offset(offset).limit(limit).all()
    sql = text("""SELECT time_bucket('1 hour', timestamp) as timestamp, 
               mode, counter ,
               sum(count_in) as count_in, 
               sum(count_out) as count_out 
               
               from counts 
               GROUP BY 1,2,3
               ORDER BY timestamp DESC""")
    results = db.execute(sql).all()
    print(results)
    return results
