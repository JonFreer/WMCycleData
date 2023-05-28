from fastapi import APIRouter, Depends
from fastapi.responses import Response
from typing import List, Union
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter()

@router.get("/counters/", response_model=List[schemas.Counter], tags=["counters"])
def read_counter(
    response: Response,
    offset: int = 0,
    limit: int = 25,
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)
    # res = crud.get_submissions(db, (limit, offset))
    # print(res[0].time)
    # return []
    print("STARTING GET")
    res = crud.read_counters(db, (limit, offset))
    print("ENDING GET")
    print(res)
    return res
