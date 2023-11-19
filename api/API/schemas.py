import datetime

from pydantic import BaseModel


class Counter(BaseModel):
    identity: int
    name: str
    lat: float
    lon: float
    location_desc: str

    class Config:
        from_attributes = True


class CounterPlus(BaseModel):
    identity: int
    name: str
    lat: float
    lon: float
    location_desc: str
    today_count: int
    this_week_count: int
    last_week_count: int
    yesterday_count: int

    class Config:
        from_attributes = True


class WeekCounts(BaseModel):
    day_of_week: int
    identity: int
    mode: str
    count_in: float
    count_out: float

    class Config:
        from_attributes = True


class Count(BaseModel):
    timestamp: datetime.datetime
    counter: int
    mode: str
    count_in: int
    count_out: int

    class Config:
        from_attributes = True
