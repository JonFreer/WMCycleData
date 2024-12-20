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
    """
    Creates or updates a CounterSummary record in the database.

    If a CounterSummary with the given identity already exists, it updates the 
    counts for today, yesterday, this week, and last week. If it does not exist, 
    it creates a new CounterSummary record with the provided counts.

    Args:
        db (Session): The database session to use for the operation.
        identity (int): The unique identifier for the CounterSummary.
        today (int): The count for today.
        yesterday (int): The count for yesterday.
        this_week (int): The count for this week.
        last_week (int): The count for last week.

    Returns:
        models.CounterSummary: The created or updated CounterSummary record.
    """
    counter_summary = db.query(models.CounterSummary).filter_by(identity=identity).first()

    if counter_summary:
        print("Updating CounterSummary")
        counter_summary.today_count = today
        counter_summary.yesterday_count = yesterday
        counter_summary.this_week_count = this_week
        counter_summary.last_week_count = last_week
    else:
        print("Creating CounterSummary")
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
) -> None:
    """
    Adds multiple count records to the database in bulk.

    Args:
        db (Session): The database session to use for the operation.
        counts (list): A list of dictionaries, each containing the count data to be added.
            Each dictionary should have the following structure:
            {
                "timestamp": <timestamp_value>,
                "mode": <mode_value>,
                "counts": {
                    "In": <count_in_value>,
                    "Out": <count_out_value>
                },
                "identity": <counter_identity>
            }

    Returns:
        None
    """
    insert_obj = counts.map(lambda count: models.Counts(timestamp=count["timestamp"],
            mode=count["mode"],
            count_in=count["counts"]["In"],
            count_out=count["counts"]["Out"],
            counter=count["identity"]))

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
    """
    Adds or updates a count record in the database.
    This function inserts a new count record into the 'counts' table or updates
    an existing record if a conflict occurs on the combination of timestamp, 
    counter, and mode. The count_in and count_out values are updated in case of 
    a conflict.
    Args:
        db (Session): The database session to use for executing the SQL command.
        counter_identity (int): The identity of the counter.
        count_in (int): The count of items coming in.
        count_out (int): The count of items going out.
        time (datetime.datetime): The timestamp of the count.
        mode (str): The mode of the count.
    Returns:
        models.Counts: The count record that was added or updated.
    """
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
    

def get_first_timestamp(
    db: Session,
    identity: int | None = None,
    modes: List[str] | None = None,
    table: str = "counts",
) -> datetime.datetime:
    """
    Retrieves the first timestamp from the specified table based on the given criteria.
    Args:
        db (Session): The database session to use for executing the query.
        identity (int | None, optional): The identity value to filter the results by. Defaults to None.
        modes (List[str] | None, optional): A list of modes to filter the results by. Defaults to None.
        table (str, optional): The name of the table to query. Defaults to "counts_hourly".
    Returns:
        datetime: The first timestamp that matches the given criteria.
    """
    table_model = getattr(models, table.capitalize())
    query = db.query(table_model.timestamp).order_by(table_model.timestamp.asc())

    if identity is not None:
        query = query.filter(table_model.counter == identity)

    if modes is not None:
        query = query.filter(table_model.mode.in_(modes))

    result = query.first()
    if result:
        return result[0]
    else:
        raise ValueError("No timestamp found for the given criteria.")
    
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

    if table is None:
        if "day" in time_interval or "month" in time_interval or "year" in time_interval:
            table = "counts_daily"
        elif "week" in time_interval:
            table = "counts_weekly"
        else:
            table = "counts"

    print("Reading Counts from table:", table, time_interval)

    if start_time is None:
        start_time = get_first_timestamp(db, identity, modes, table).timestamp()

    sql_string = f"""
        SELECT time_bucket_gapfill(:time_interval, timestamp) as timestamp, 
                mode, counter,
                COALESCE(sum(count_in), 0) AS count_in,
                COALESCE(sum(count_out), 0) AS count_out
        FROM {table}
        WHERE """

    if identity is not None:
        sql_string += "counter = :identity AND "

    if modes is not None:
        modes_str = ",".join(f"'{mode}'" for mode in modes)
        sql_string += f"mode IN ({modes_str}) AND "

    sql_string += """
        timestamp > TIMESTAMPTZ :start_time AND timestamp <= TIMESTAMPTZ :end_time
        GROUP BY 1, 2, 3
        ORDER BY timestamp DESC
        LIMIT :limit OFFSET :offset
    """

    sql = text(sql_string)

    if end_time is None:
        end_time = datetime.datetime.now().timestamp()

    sql = sql.bindparams(
        bindparam("time_interval", value=time_interval),
        bindparam("start_time", value=datetime.datetime.fromtimestamp(start_time)),
        bindparam("end_time", value=datetime.datetime.fromtimestamp(end_time)),
        bindparam("limit", value=limit),
        bindparam("offset", value=offset),
    )

    if identity is not None:
        sql = sql.bindparams(bindparam("identity", value=identity))

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
    """
    Reads the average counts from the database within a specified time range and optional filters.

    Args:
        db (Session): The database session to use for the query.
        identity (int | None, optional): The identity of the counter to filter by. Defaults to None.
        start_time (int | None, optional): The start time (timestamp) for the query. Defaults to None.
        end_time (int | None, optional): The end time (timestamp) for the query. Defaults to None.
        modes (List[str] | None, optional): A list of modes to filter by. Defaults to None.
        table (str, optional): The name of the table to query from. Defaults to "counts_daily".

    Returns:
        List[schemas.WeekCounts]: A list of average counts grouped by day of the week, counter, and mode.
    """
    where_clauses = ["timestamp > TIMESTAMPTZ :start_time", "timestamp <= TIMESTAMPTZ :end_time"]

    if identity is not None:
        where_clauses.append("counter = :identity")

    if modes is not None:
        where_clauses.append("mode IN ({})".format(",".join("'{0}'".format(x) for x in modes)))

    where_string = " AND ".join(where_clauses)

    sql = text(f"""
        SELECT
            EXTRACT(ISODOW FROM timestamp) AS day_of_week, 
            counter as identity,
            mode,
            AVG(count_in) AS count_in,
            AVG(count_out) AS count_out
        FROM
            {table}
        WHERE {where_string}
        GROUP BY
            counter, mode, day_of_week
        ORDER BY
            day_of_week;
    """)

    if end_time is None:
        end_time = datetime.datetime.now().timestamp()
    if start_time is None:
        start_time = 0

    sql = sql.bindparams(
        bindparam("identity", value=identity),
        bindparam("start_time", value=datetime.datetime.fromtimestamp(start_time)),
        bindparam("end_time", value=datetime.datetime.fromtimestamp(end_time)),
    )

    results = db.execute(sql).all()
    return results
