from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from typing import Annotated
from typing import List, Union
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db
import datetime
router = APIRouter()

DAY_SECONDS = 86400

@router.get("/counters/", response_model=List[schemas.Counter], tags=["counters"])
def read_counter(
    response: Response,
    offset: int = 0,
    limit: Annotated[int, Query(title="Limit", description="Number of count values returned")] = 25,
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)
    res = crud.read_counters(db, (limit, offset))
    return res

@router.get("/counts/", response_model=List[schemas.Count], tags=["counters"])
def read_all_counts(
    response: Response,
    identity : int | None = None,
    offset: int = 0,
    limit: int = 25,
    time_interval:str = "1 hour",
    db: Session = Depends(get_db),
    
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)
    if (identity==None):
        return crud.read_all_counts(db, (limit, offset),time_interval=time_interval)
    else: 
        return crud.read_counts(db, (limit, offset),time_interval=time_interval,identity=identity,start_time=0)

#Returns all the counters plus key stats
@router.get("/counters_plus/", response_model=List[schemas.CounterPlus], tags=["counters"])
def read_counter_plus(
    response: Response,
    offset: int = 0,
    limit: Annotated[int|None, Query(title="Limit", description="Optional: Number of count values returned")] = None,
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)
    counters = crud.read_counters(db, (limit, offset))
    response = []
    for counter in counters:
        today = 0
        yesterday = 0
        week_count = 0

        today_res = crud.read_counts(db, (None, 0),time_interval="1 day",identity=counter.identity,start_time=int(datetime.datetime.now().timestamp()-DAY_SECONDS*2))
        week_res = crud.read_counts(db, (None, 0),time_interval="1 week",identity=counter.identity,start_time=int(datetime.datetime.now().timestamp()-DAY_SECONDS*7))

        today_res = list(filter(lambda x: (x.mode == "cyclist"), today_res)) 
        week_res = list(filter(lambda x: (x.mode == "cyclist"), week_res)) 

        if(len(today_res) > 0):
            today= today_res[0].count_in + today_res[0].count_out
       
        if(len(today_res) > 1):
            yesterday= today_res[1].count_in + today_res[1].count_out
        
        if(len(week_res) > 0):
            week_count= week_res[0].count_in + week_res[0].count_out

        response.append(
            schemas.CounterPlus(
                identity=counter.identity,
                name=counter.name,
                lat= counter.lat,
                lon = counter.lon,
                location_desc = counter.location_desc,
                today_count = today,
                week_count = week_count,
                yesterday_count = yesterday
            )
        )
    return response

@router.get("/today/", response_model=List[schemas.Count], tags=["counters"])
def read_today(
    response: Response,
    identity: int,
    # start_time:int = dat,
    # offset: int = 0,
    # limit: int = 25,
    # time_interval:str = "1 hour",
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)

    res = crud.read_counts(db, (None, 0),time_interval="1 day",identity=identity,start_time=int(datetime.datetime.now().timestamp()-86400))

    return res

