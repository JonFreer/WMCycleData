from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from fastapi.security.api_key import APIKey
from sqlalchemy.orm import Session

from .. import crud, loader, schemas, tasks
from ..dependencies import get_db
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
    return crud.create_counter(db, identity, name, lat, lon, location_desc)


@router.post("/add_count/", response_model=schemas.Count, tags=["admin"])
def add_count(
    response: Response,
    api_key: Annotated[APIKey, Depends(auth.get_api_key)],
    count_in: int,
    count_out: int,
    counter: str,
    db: Session = Depends(get_db),
):
    response.headers["X-Total-Count"] = str(5)
    try:
        res = crud.add_count(db, counter, count_in, count_out)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return res


# Load counters from wmcycledata.com/api for dev purposes
@router.post(
    "/load_dummy_counters/",
    status_code=201,
    tags=["admin"],
    summary="Load counters from exisiting db at wmcycledata.com",
)
def load_dummy_counters(
    api_key: Annotated[APIKey, Depends(auth.get_api_key)],
    db: Session = Depends(get_db),
):
    response = requests.get("https://wmcycledata.com/api/counters")
    response.raise_for_status()
    counters = response.json()

    for counter in counters:
        print(counter)
        crud.create_counter(
            db,
            counter["identity"],
            counter["name"],
            counter["lat"],
            counter["lon"],
            counter["location_desc"],
        )

    return Response(status_code=status.HTTP_201_CREATED)


# Load counts from wmcycledata.com/api for dev purposes
@router.post(
    "/load_dummy_counts/",
    status_code=201,
    tags=["admin"],
    summary="Load counts from exisiting db at wmcycledata.com",
)
def load_dummy_counts(
    api_key: Annotated[APIKey, Depends(auth.get_api_key)],
    start_time: int | None,
    db: Session = Depends(get_db),
):
    if start_time != None:
        response = requests.get(
            "https://wmcycledata.com/api/counts?start_time=" + str(start_time)
        )
    else:
        response = requests.get("https://wmcycledata.com/api/counts")

    response.raise_for_status()
    counts = response.json()

    crud.add_count_time_bulk(counts)

    return Response(status_code=status.HTTP_201_CREATED)


# Request Vivacity counts and add them to the database
@router.post(
    "/load_vivacity/",
    status_code=202,
    response_model=schemas.Job,
    tags=["admin"],
    summary="Queue a Vivacity load",
    description="Queue a background job that requests the counts for each counter in the counters table, stores them in the counts table and rebuilds the cached summaries. Returns immediately: poll /jobs/{job_id} for the outcome.",
)
def load_vivacity(
    api_key: Annotated[APIKey, Depends(auth.get_api_key)],
    identity: Annotated[
        int | None,
        Query(
            title="Identity",
            description="Optional. Leave blank to load data for all counters",
        ),
    ] = None,
    delta_t: int = (4 * 60 * 60),
    end_t: int | None = None,
):
    return tasks.submit(
        "load_vivacity",
        loader.load_vivacity_counts,
        delta_t=delta_t,
        identity=identity,
        end_t=end_t,
    )


@router.get(
    "/jobs/",
    response_model=list[schemas.Job],
    tags=["admin"],
    summary="Recently queued background jobs",
)
def read_jobs(api_key: Annotated[APIKey, Depends(auth.get_api_key)]):
    return tasks.recent()


@router.get(
    "/jobs/{job_id}",
    response_model=schemas.Job,
    tags=["admin"],
    summary="Status of a single background job",
)
def read_job(job_id: str, api_key: Annotated[APIKey, Depends(auth.get_api_key)]):
    job = tasks.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="No such job")
    return job
