import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter()

DAY_SECONDS = 86400


@router.get("/counters/", response_model=List[schemas.Counter], tags=["counters"])
def read_counter(
    response: Response,
    offset: int = 0,
    limit: Annotated[
        int, Query(title="Limit", description="Number of count values returned")
    ] = 25,
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)
    res = crud.read_counters(db, (limit, offset))
    return res


@router.get("/counts/", response_model=List[schemas.Count], tags=["counters"])
def read_counts(
    response: Response,
    identity: int | None = None,
    start_time: Annotated[
        int | None,
        Query(
            title="Start Time", description="Start timestamp of data. Defaults to zero."
        ),
    ] = None,
    end_time: Annotated[
        int | None,
        Query(
            title="End Time",
            description="End timestamp of data. Defaults to current time.",
        ),
    ] = None,
    offset: int = 0,
    limit: int = 25,
    time_interval: str = "1 hour",
    modes: List[str] = Query(
        None,
        description="""Mode of transport. Leave blank to return values for all modes. 
                            List of available modes: cyclist, car, pedestrian, truck, motorbike, escooter, bus, van, rigid, taxi, minibus, emergency_car, emergency_van, fire_engine, cargo_bicycle, rental_bicycle. """,
    ),
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)

    if modes != None:
        check_modes(modes)

    return crud.read_counts(
        db,
        (limit, offset),
        time_interval=time_interval,
        identity=identity,
        start_time=start_time,
        end_time=end_time,
        modes=modes,
    )


@router.get(
    "/average_week/", response_model=List[schemas.WeekCounts], tags=["counters"]
)
def AverageWeek(
    response: Response,
    identity: int | None = None,
    start_time: Annotated[
        int | None,
        Query(
            title="Start Time", description="Start timestamp of data. Defaults to zero."
        ),
    ] = None,
    end_time: Annotated[
        int | None,
        Query(
            title="End Time",
            description="End timestamp of data. Defaults to current time.",
        ),
    ] = None,
    modes: List[str] = Query(
        None,
        description="""Mode of transport. Leave blank to return values for all modes. 
                            List of available modes: cyclist, car, pedestrian, truck, motorbike, escooter, bus, van, rigid, taxi, minibus, emergency_car, emergency_van, fire_engine, cargo_bicycle, rental_bicycle. """,
    ),
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)

    if modes != None:
        check_modes(modes)

    return crud.read_average(
        db,
        identity=identity,
        start_time=start_time,
        end_time=end_time,
        modes=modes,
    )


# Returns all the counters plus key stats
@router.get(
    "/counters_plus/", response_model=List[schemas.CounterPlus], tags=["counters"]
)
def read_counter_plus(
    response: Response,
    offset: int = 0,
    limit: Annotated[
        int | None,
        Query(title="Limit", description="Optional: Number of count values returned"),
    ] = None,
    db: Session = Depends(get_db),
):
    response.headers["X-Total-Count"] = str(5)
    counters = crud.read_counters_plus(db, (limit, offset))
    return counters


@router.get("/today/", response_model=List[schemas.Count], tags=["counters"])
def read_today(
    response: Response,
    identity: int,
    db: Session = Depends(get_db),
):
    # validate.check_limit(limit)
    response.headers["X-Total-Count"] = str(5)

    res = crud.read_counts(
        db,
        (None, 0),
        time_interval="1 day",
        identity=identity,
        start_time=int(datetime.datetime.now().timestamp() - 86400),
    )

    return res


def check_modes(modes: List[str]):
    MODES = set(
        [
            "cyclist",
            "car",
            "pedestrian",
            "truck",
            "motorbike",
            "escooter",
            "bus",
            "van",
            "rigid",
            "taxi",
            "minibus",
            "emergency_car",
            "emergency_van",
            "fire_engine",
            "cargo_bicycle",
            "rental_bicycle",
        ]
    )
    modes_diff = set(modes) - MODES
    if len(modes_diff) != 0:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid modes: {modes_diff}",
        )
