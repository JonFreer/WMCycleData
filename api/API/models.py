from .db import Base, engine
import uuid
from sqlalchemy.dialects.postgresql import JSONB, UUID
# from sqlalchemy.types import TIMESTAMP
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Float, Integer, BigInteger, event, DDL,orm,UniqueConstraint

# Base = orm.declarative_base()

class Counter(Base):
    __tablename__ = "counters"
    name = Column(
        String, primary_key=True, index=True, default=uuid.uuid4
    )
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    location_desc = Column(String, nullable=True)


class Counts(Base):
    __tablename__ = 'counts'
    # __table_args__ = (UniqueConstraint("msg_id", "timestamp"),)
    id = Column(Integer, primary_key=True, autoincrement=True)
    counter = Column(String, nullable = False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True, primary_key=True)
    count_in = Column(Integer , nullable = False)
    count_out = Column(Integer , nullable = False)

event.listen(
    Counts.__table__,
    'after_create',
    DDL(f"SELECT create_hypertable('{Counts.__tablename__}', 'timestamp');")
)