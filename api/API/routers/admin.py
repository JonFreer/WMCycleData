
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import Response
from fastapi.security.api_key import APIKey

from typing import List, Union
from sqlalchemy.orm import Session
from typing import Annotated

from .. import crud, schemas, vivacity
from ..dependencies import get_db
from .. import config
from . import auth

router = APIRouter()

@router.post("/add_counter/", response_model=schemas.Counter, tags=["admin"])
def add_counter(
    response: Response,
    api_key: Annotated[APIKey, Depends(auth.get_api_key)],
    identity: int,
    name: str,
    lat: float,
    lon: float,
    location_desc: str = "", 
    db: Session = Depends(get_db),
):
    response.headers["X-Total-Count"] = str(5)
    return crud.create_counter(db,identity, name,lat,lon,location_desc)

@router.post("/add_count/", response_model=schemas.Count, tags=["admin"])
def add_count(
    response: Response,
    api_key: Annotated[APIKey, Depends(auth.get_api_key)],
    count_in: int,
    count_out:int,
    counter:str,
    db: Session = Depends(get_db),
):
    response.headers["X-Total-Count"] = str(5)
    try:
        res = crud.add_count(db, counter,count_in,count_out)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
    return res

# Request Vivacity counts and add them to the database
@router.post("/load_vivacity/", 
             status_code=201, 
             tags=["admin"],
             summary="Request Vivacity counts and add them to the database",
             description ="Iterate through each of the counters stored in the counters table. Request the counts for each of the counters. Store the counts in the counts table."
             )
def load_vivacity(response: Response,
                  api_key: Annotated[APIKey, Depends(auth.get_api_key)],
                  delta_t :int = (4*60*60),
                  db: Session = Depends(get_db),
                  ):

    counters = crud.read_counters(db,[None,0])
    modes = ["cyclist","escooter","rental_bicycle"]
    for mode in modes:
        for counter in counters:  
            results = vivacity.Vivacity.get_counts(counter.identity,config.VivacityKey,mode,delta_t)
            for time in results:
                crud.add_count_time(db,counter.identity,results[time]["In"],results[time]["Out"],time,mode)

    return Response(status_code=status.HTTP_201_CREATED)