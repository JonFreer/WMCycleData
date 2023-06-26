import datetime

from pydantic import BaseModel


class Counter(BaseModel):
    identity: int
    name: str
    lat: float
    lon: float
    location_desc: str

    class Config:
        orm_mode = True


class CounterPlus(BaseModel):
    identity: int
    name: str
    lat: float
    lon: float
    location_desc: str
    today_count: int
    week_count: int
    last_week_count: int
    yesterday_count: int

    class Config:
        orm_mode = True


class Count(BaseModel):
    timestamp: datetime.datetime
    counter: int
    mode: str
    count_in: int
    count_out: int

    class Config:
        orm_mode = True
