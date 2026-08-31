from sqlalchemy import DDL, Column, DateTime, Float, Integer, String, event

from .db import Base


class Counter(Base):
    __tablename__ = "counters"
    identity = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    location_desc = Column(String, nullable=True)


class CounterSummary(Base):
    __tablename__ = "counts_summary"
    identity = Column(Integer, nullable=False, primary_key=True)
    today_count = Column(Integer, nullable=False)
    yesterday_count = Column(Integer, nullable=False)
    this_week_count = Column(Integer, nullable=False)
    last_week_count = Column(Integer, nullable=False)


class Counts(Base):
    __tablename__ = "counts"
    counter = Column(Integer, nullable=False, primary_key=True)
    timestamp = Column(
        DateTime(timezone=True), nullable=False, index=True, primary_key=True
    )
    mode = Column(String, nullable=False, primary_key=True)
    count_in = Column(Integer, nullable=False)
    count_out = Column(Integer, nullable=False)

class Counts_daily(Base):
    __tablename__ = "counts_daily"
    counter = Column(Integer, nullable=False, primary_key=True)
    timestamp = Column(
        DateTime(timezone=True), nullable=False, index=True, primary_key=True
    )
    mode = Column(String, nullable=False, primary_key=True)
    count_in = Column(Integer, nullable=False)
    count_out = Column(Integer, nullable=False)

class Counts_weekly(Base):
    __tablename__ = "counts_weekly"
    counter = Column(Integer, nullable=False, primary_key=True)
    timestamp = Column(
        DateTime(timezone=True), nullable=False, index=True, primary_key=True
    )
    mode = Column(String, nullable=False, primary_key=True)
    count_in = Column(Integer, nullable=False)
    count_out = Column(Integer, nullable=False)


class JobState(Base):
    __tablename__ = "job_state"
    name = Column(String, primary_key=True)
    # When the scheduler last queued this job, so a restart does not reset the
    # clock, and how far back_load has walked into the archive.
    last_run = Column(DateTime(timezone=True), nullable=False)
    cursor = Column(Integer, nullable=False, default=0)


# Mapped so they can be queried, but db_init builds them as TimescaleDB
# continuous aggregates, so create_all() must not make plain tables of them.
CONTINUOUS_AGGREGATES = (Counts_daily.__table__, Counts_weekly.__table__)


# event.listen(
#     Counts.__table__,
#     "after_create",
#     DDL(
#         f"""
#         SELECT create_hypertable('{Counts.__tablename__}', 'timestamp');

#         CREATE MATERIALIZED VIEW counts_hourly
#             WITH (timescaledb.continuous) AS
#             SELECT
#             time_bucket('1 hour', timestamp) as timestamp,
#             mode, counter,
#             sum(count_in) as count_in, 
#             sum(count_out) as count_out 
#             FROM counts
#             GROUP BY 1,2,3
#             WITH NO DATA;

#         SELECT add_continuous_aggregate_policy('counts_hourly',
#             start_offset => INTERVAL '4 hours',
#             end_offset => NULL,
#             schedule_interval => INTERVAL '30 minutes');

#         """
#     ),
# )

# CALL refresh_continuous_aggregate('counts_hourly', NULL, NULL);
