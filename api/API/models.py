from .db import Base, engine
import uuid
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String,Float,Integer,BigInteger

class Counter(Base):
    __tablename__ = "counters"
    name = Column(
        String, primary_key=True, index=True, default=uuid.uuid4
    )
    lat = Column(Float,nullable=False)
    lon = Column(Float,nullable=False)
    location_desc = Column(String,nullable=True)
