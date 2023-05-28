from datetime import datetime
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import or_,and_

from . import config, models
from typing import Any, Dict, List, Optional, Tuple, Union

def read_counters(db: Session, limit_offset: Tuple[int, int])->List[models.Counter]:
    limit, offset = limit_offset
    counters = db.query(models.Counter).offset(offset).limit(limit).all()
    return counters

def create_counter(db:Session, name:str, lat:float,lon:float,location_desc:str)->models.Counter:
    print("Creating Counter")
    db_submission = models.Counter( 
        name=name,
        lat=lat,
        lon=lon,
        location_desc=location_desc)

    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission