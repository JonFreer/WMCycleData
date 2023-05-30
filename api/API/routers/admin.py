
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from typing import List, Union
from sqlalchemy.orm import Session

from .. import crud, schemas
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
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)
    # res = crud.get_submissions(db, (limit, offset))
    # print(res[0].time)
    # return []
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