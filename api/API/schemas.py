from pydantic import BaseModel
import uuid
import datetime

class Counter(BaseModel):
    name:str
    lat:float
    lon:float
    location_desc:str

    class Config:
        orm_mode = True

class Count(BaseModel):
    id: int
    timestamp:datetime.datetime
    count:int

    class Config:
        orm_mode = True