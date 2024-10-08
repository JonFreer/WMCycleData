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

# This may be redundant, think about moving
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

def add_count_time_bulk(
    db: Session,
    counts: list
) -> models.Counts:

    insert_obj = []
    for count in counts:
        insert_obj.append(models.Counts(
            timestamp=count["timestamp"],
            mode=count["mode"],
            count_in=count["counts"]["In"],
            count_out=count["counts"]["Out"],
            counter=count["identity"],
        ))

    db.bulk_save_objects(insert_obj)
    db.commit()

def add_count_time(
    db: Session,
    counter_identity: int,
    count_in: int,
    count_out: int,
    time: datetime.datetime,
    mode: str,
) -> models.Counts:
    # # Validate if the counter is valid

    sql_text = """INSERT INTO counts
                    VALUES (:counter, TIMESTAMPTZ :timestamp, :mode, :count_in, :count_out)
                    ON CONFLICT (timestamp, counter, mode) DO UPDATE
                    SET count_in = excluded.count_in,
                    count_out = excluded.count_out;"""
    
    sql = text(sql_text)
    
    sql = sql.bindparams(
        bindparam("counter", value=counter_identity),
        bindparam("timestamp", value=time),
        bindparam("mode", value=mode),
        bindparam("count_in", value=count_in),
        bindparam("count_out", value=count_out),
    )

    db.execute(sql)

    # db_submission = models.Counts(
    #     timestamp=time,
    #     mode=mode,
    #     count_in=count_in,
    #     count_out=count_out,
    #     counter=counter_identity,
    # )
    # db.merge(db_submission)
    # db.commit()

    # query = (
    #     db.query(models.Counts)
    #     .where(models.Counts.counter == counter_identity)
    #     .where(models.Counts.timestamp == time)
    #     .where(models.Counts.mode == mode)
    # )

    # db_submission = query.first()

    # if db_submission:  # If value in db update
    #     db_submission.count_in = count_in
    #     db_submission.count_out = count_out
    #     print("updating")
    # else:  # If value not in db, add it to the db
    #     db_submission = models.Counts(
    #         timestamp=time,
    #         mode=mode,
    #         count_in=count_in,
    #         count_out=count_out,
    #         counter=counter_identity,
    #     )
    #     db.add(db_submission)

    # db.commit()
    # db.refresh(db_submission)

    # return db_submission


def get_first_timestamp(
    db: Session,
    identity: int | None = None,
    modes: List[str] | None = None,
    table: str = "counts",
) -> datetime:
    
    time_string = (
            """SELECT first(timestamp,timestamp) FROM {} WHERE """).format(table)

    if identity != None:
        time_string = time_string + "counter = :identity AND "

    if modes != None:
        time_string = (
            time_string
            + "mode IN ({})".format(",".join("'{0}'".format(x) for x in modes))
        )

    sql = text(time_string)

    if identity != None:
        sql = sql.bindparams(
            bindparam("identity", value=identity),
        )

    return db.execute(sql).all()[0][0]

def read_counts(
    db: Session,
    limit_offset: Tuple[int, int],
    time_interval: str,
    identity: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    modes: List[str] | None = None,
    table: str | None = None,
) -> List[models.Counts]:
    limit, offset = limit_offset

    if table == None:
        if "day" in time_interval or "month" in time_interval or "year" in time_interval:
            table = "counts_daily"
        elif "week" in time_interval:
            table = "counts_weekly"
        else:
            table = "counts"

    print("Reading Counts from table:", table,time_interval)

    if start_time == None:
        start_time = get_first_timestamp(db,identity,modes,table).timestamp()
   
    #If start time is None, and we want gapfill, then we need to first query to find the first item and then gapfill from there

    sql_string = (
        """
  
        SELECT time_bucket_gapfill(:timeInterval , timestamp) as timestamp, 
               mode, counter ,
               CASE WHEN sum(count_in) IS NULL THEN 0 ELSE sum(count_in) END AS count_in,
               CASE WHEN sum(count_out) IS NULL THEN 0 ELSE sum(count_out) END AS count_out
               FROM {} WHERE """.format(table)
    )

    if identity != None:
        sql_string = sql_string + "counter = :identity AND "

    if modes != None:
        sql_string = (
            sql_string
            + "mode IN ("
            + ",".join("'{0}'".format(x) for x in modes)
            + ") AND "
        )

    sql_string = (
        sql_string
        + """  timestamp > TIMESTAMPTZ :start_time AND timestamp <= TIMESTAMPTZ :end_time
               GROUP BY 1,2,3
               ORDER BY timestamp DESC""" #timestamp > TIMESTAMPTZ :start_time AND
    )

    sql = text(sql_string)

    if end_time == None:
        end_time = datetime.datetime.now().timestamp()
    
    sql = sql.bindparams(
        bindparam("timeInterval", value=time_interval),
        bindparam("start_time", value=datetime.datetime.fromtimestamp(start_time)),
        bindparam("end_time", value=datetime.datetime.fromtimestamp(end_time)),
        # bindparam("table", value=table),
    )

    if identity != None:
        sql = sql.bindparams(
            bindparam("identity", value=identity),
        )

    results = db.execute(sql).all()
    return results


def read_average(
    db: Session,
    identity: int | None = None,
    start_time: int | None = None,
    end_time: int | None = None,
    modes: List[str] | None = None,
    table: str = "counts_daily",
) -> List[schemas.WeekCounts]:
    
    where_string = ""

    if identity != None:
        where_string =  "AND counter = :identity "

    if modes != None:
        where_string = (where_string + " AND mode IN ({})").format( ",".join("'{0}'".format(x) for x in modes))
      

    sql = ("""
            SELECT
                EXTRACT(ISODOW FROM timestamp) AS day_of_week, 
                counter as identity,
                mode,
                AVG(count_in) AS count_in,
                AVG(count_out) AS count_out
            FROM
                counts_daily
            WHERE timestamp > TIMESTAMPTZ :start_time
               AND timestamp <= TIMESTAMPTZ :end_time {}
            GROUP BY
                counter,mode,day_of_week
            ORDER BY
                day_of_week;""").format(where_string)

    sql = text(sql)

    if end_time == None:
        end_time = datetime.datetime.now().timestamp()
    if start_time == None:
        start_time = 0

    sql = sql.bindparams(
        bindparam("identity", value=identity),
        bindparam("start_time", value=datetime.datetime.fromtimestamp(start_time)),
        bindparam("end_time", value=datetime.datetime.fromtimestamp(end_time)),
    )
    results = db.execute(sql).all()
    return results
