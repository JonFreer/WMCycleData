
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import Response
from typing import List, Union
from sqlalchemy.orm import Session

from .. import crud, schemas, vivacity
from ..dependencies import get_db

router = APIRouter()

@router.post("/add_counter/", response_model=schemas.Counter, tags=["admin"])
def add_counter(
    response: Response,
    name: str,
    lat: float,
    lon: float,
    location_desc: str = "", 
    db: Session = Depends(get_db),
):
    response.headers["X-Total-Count"] = str(5)
    return crud.create_counter(db, name,lat,lon,location_desc)

@router.post("/add_count/", response_model=schemas.Count, tags=["admin"])
def add_count(
    response: Response,
    count_in: int,
    count_out:int,
    counter:str,
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)
    # res = crud.get_submissions(db, (limit, offset))
    # print(res[0].time)
    # return []
    print("STARTING GET")

    try:
        res = crud.add_count(db, counter,count_in,count_out)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    print("ENDING GET")
    print(res)
    return res

# Request Vivacity counts and add them to the database
@router.post("/load_vivacity/", 
             status_code=201, 
             tags=["admin"],
             summary="Request Vivacity counts and add them to the database",
             description ="Iterate through each of the counters stored in the counters table. Request the counts for each of the counters. Store the counts in the counts table."
             )
def load_vivacity(response: Response,
                  api_key:str,
                  db: Session = Depends(get_db)):
    
    counters = crud.read_counters(db,[None,0])
    mode = "cyclist"

    for counter in counters:  
        results = vivacity.Vivacity.get_counts(counter.name,api_key,mode)
        for time in results:
            crud.add_count_time(db,counter.name,results[time]["In"],results[time]["Out"],time,mode)

    return Response(status_code=status.HTTP_201_CREATED)