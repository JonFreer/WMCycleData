
from fastapi import APIRouter, Depends
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
    count: int,
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)
    # res = crud.get_submissions(db, (limit, offset))
    # print(res[0].time)
    # return []
    print("STARTING GET")
    res = crud.add_count(db, count)
    print("ENDING GET")
    print(res)
    return res