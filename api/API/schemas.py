from pydantic import BaseModel
import uuid

class Counter(BaseModel):
    name:str
    lat:float
    lon:float
    location_desc:str
