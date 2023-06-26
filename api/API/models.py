from sqlalchemy import DDL, Column, DateTime, Float, Integer, String, event

from .db import Base


class Counter(Base):
    __tablename__ = "counters"
    identity = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    location_desc = Column(String, nullable=True)


class Counts(Base):
    __tablename__ = "counts"
    counter = Column(Integer, nullable=False, primary_key=True)
    timestamp = Column(
        DateTime(timezone=True), nullable=False, index=True, primary_key=True
    )
    mode = Column(String, nullable=False, primary_key=True)
    count_in = Column(Integer, nullable=False)
    count_out = Column(Integer, nullable=False)


event.listen(
    Counts.__table__,
    "after_create",
    DDL(f"SELECT create_hypertable('{Counts.__tablename__}', 'timestamp');"),
)
