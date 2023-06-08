from pydantic import BaseModel
import uuid
import datetime

class Counter(BaseModel):
    identity:int
    name:str
    lat:float
    lon:float
    location_desc:str

    class Config:
        orm_mode = True

class Count(BaseModel):
    timestamp:datetime.datetime
    counter: str
    mode:str
    count_in:int
    count_out:int

    class Config:
        orm_mode = True