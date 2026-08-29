"""TimescaleDB objects that SQLAlchemy's create_all() cannot build.

`counts` has to be a hypertable, and counts_daily / counts_weekly have to be
continuous aggregates rather than the plain tables their models describe. This
runs on every start, straight after create_all(), and is a no-op once the
objects are in place.
"""

from sqlalchemy import text
from sqlalchemy.engine import Engine

# (view, bucket, source). counts_weekly rolls up counts_daily, so order matters.
AGGREGATES = [
    ("counts_daily", "1 day", "counts"),
    ("counts_weekly", "1 week", "counts_daily"),
]

# view -> (start_offset, schedule_interval) for the refresh policy.
POLICIES = {
    "counts_daily": ("2 days", "12 hours"),
    "counts_weekly": ("1 month", "7 days"),
}


def _scalar(conn, sql: str, **params):
    return conn.execute(text(sql), params).scalar()


def _is_hypertable(conn, name: str) -> bool:
    return _scalar(
        conn,
        """SELECT count(*) FROM timescaledb_information.hypertables
           WHERE hypertable_schema = 'public' AND hypertable_name = :name""",
        name=name,
    ) > 0


def _is_continuous_aggregate(conn, name: str) -> bool:
    return _scalar(
        conn,
        """SELECT count(*) FROM timescaledb_information.continuous_aggregates
           WHERE view_schema = 'public' AND view_name = :name""",
        name=name,
    ) > 0


def _has_refresh_policy(conn, name: str) -> bool:
    return _scalar(
        conn,
        """SELECT count(*) FROM timescaledb_information.jobs
           WHERE proc_name = 'policy_refresh_continuous_aggregate'
             AND hypertable_schema = 'public' AND hypertable_name = :name""",
        name=name,
    ) > 0


def _relkind(conn, name: str) -> str | None:
    return _scalar(
        conn,
        """SELECT relkind FROM pg_class
           WHERE relnamespace = 'public'::regnamespace AND relname = :name""",
        name=name,
    )


def _drop_placeholder_table(conn, name: str) -> None:
    """Remove the empty table create_all() leaves behind for an aggregate.

    Only an empty plain table is dropped: anything holding rows is somebody's
    data, so we leave it alone and let the aggregate creation fail loudly.
    """
    if _relkind(conn, name) != "r":
        return

    rows = _scalar(conn, f"SELECT count(*) FROM {name}")
    if rows:
        raise RuntimeError(
            f"{name} is a plain table holding {rows} rows, but it should be a "
            f"continuous aggregate. Move the data aside and restart."
        )

    print(f"db_init: dropping empty placeholder table {name}")
    conn.execute(text(f"DROP TABLE {name}"))


def _create_aggregate(conn, view: str, bucket: str, source: str) -> None:
    print(f"db_init: creating continuous aggregate {view}")
    conn.execute(
        text(
            f"""
            CREATE MATERIALIZED VIEW {view}
            WITH (timescaledb.continuous) AS
            SELECT time_bucket('{bucket}', timestamp) AS timestamp,
                   mode, counter,
                   sum(count_in) AS count_in,
                   sum(count_out) AS count_out
            FROM {source}
            GROUP BY 1, 2, 3
            """
        )
    )
    # Real-time aggregation, so buckets newer than the last refresh still show up.
    conn.execute(
        text(
            f"ALTER MATERIALIZED VIEW {view} "
            f"SET (timescaledb.materialized_only = false)"
        )
    )


def init_timescale(engine: Engine) -> None:
    # create_hypertable, CREATE MATERIALIZED VIEW ... continuous and the policy
    # calls all refuse to run inside a transaction block.
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        if not _is_hypertable(conn, "counts"):
            print("db_init: converting counts into a hypertable")
            conn.execute(
                text(
                    "SELECT create_hypertable('counts', by_range('timestamp'), "
                    "migrate_data => true)"
                )
            )

        for view, bucket, source in AGGREGATES:
            if not _is_continuous_aggregate(conn, view):
                _drop_placeholder_table(conn, view)
                _create_aggregate(conn, view, bucket, source)

            if not _has_refresh_policy(conn, view):
                start_offset, schedule_interval = POLICIES[view]
                print(f"db_init: adding refresh policy for {view}")
                conn.execute(
                    text(
                        "SELECT add_continuous_aggregate_policy(:view, "
                        "start_offset => CAST(:start_offset AS INTERVAL), "
                        "end_offset => NULL, "
                        "schedule_interval => CAST(:schedule_interval AS INTERVAL))"
                    ),
                    {
                        "view": view,
                        "start_offset": start_offset,
                        "schedule_interval": schedule_interval,
                    },
                )
