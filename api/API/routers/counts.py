from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from typing import Annotated
from typing import List, Union
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter()

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
    offset: int = 0,
    limit: int = 25,
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)
    res = crud.read_all_counts(db, (limit, offset))
    return res

