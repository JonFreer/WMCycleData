import datetime
from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from fastapi.security.api_key import APIKey
from sqlalchemy.orm import Session

from .. import config, crud, schemas, vivacity
from ..dependencies import get_db
from . import auth

DAY_SECONDS = 86400

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

    for count in counts:
        # print(counter)
        try:
            crud.add_count_time(
                db,
                count["counter"],
                count["count_in"],
                count["count_out"],
                count["timestamp"],
                count["mode"],
            )
        except:
            pass

    return Response(status_code=status.HTTP_201_CREATED)


# Request Vivacity counts and add them to the database
@router.post(
    "/load_vivacity/",
    status_code=201,
    tags=["admin"],
    summary="Request Vivacity counts and add them to the database",
    description="Iterate through each of the counters stored in the counters table. Request the counts for each of the counters. Store the counts in the counts table.",
)
def load_vivacity(
    response: Response,
    api_key: Annotated[APIKey, Depends(auth.get_api_key)],
    identity: Annotated[
        int | None,
        Query(
            title="Identity",
            description="Optional. Leave blank to load data for all counters",
        ),
    ] = None,
    delta_t: int = (4 * 60 * 60),
    db: Session = Depends(get_db),
):
    counters = crud.read_counters(db, [None, 0])

    results, counters_vivacity = vivacity.Vivacity.get_counts(
        config.VivacityKey, delta_t, identity
    )

    # Add any new counters to the counters table

    counters_identitys = map(lambda x: x.identity, counters)
    new_counters = set(counters_vivacity).difference(set(counters_identitys))

    print("counters_identity", new_counters)

    for counter_id in new_counters:
        crud.create_counter(
            db,
            counter_id,
            "",
            counters_vivacity[counter_id].split(",")[0],
            counters_vivacity[counter_id].split(",")[1],
            "",
        )

    for count in results:
        print(count)
        crud.add_count_time(
            db,
            count["identity"],
            count["counts"]["In"],
            count["counts"]["Out"],
            count["timestamp"],
            count["mode"],
        )

    # Update cached summary
    # Iterate through each counter and calculate daily and weekly summaries
    counters = crud.read_counters(db, (None, 0))

    for counter in counters:
        today = 0
        yesterday = 0
        week_count = 0
        last_week_count = 0

        today_res = crud.read_counts(
            db,
            (None, 0),
            time_interval="1 day",
            identity=counter.identity,
            start_time=int(datetime.datetime.now().timestamp() - DAY_SECONDS * 2),
            table="counts",
        )
        week_res = crud.read_counts(
            db,
            (None, 0),
            time_interval="1 week",
            identity=counter.identity,
            start_time=int(datetime.datetime.now().timestamp() - DAY_SECONDS * 14),
            table="counts",
        )

        today_res = list(filter(lambda x: (x.mode == "cyclist"), today_res))
        week_res = list(filter(lambda x: (x.mode == "cyclist"), week_res))

        if len(today_res) > 0:
            today = today_res[0].count_in + today_res[0].count_out

        if len(today_res) > 1:
            yesterday = today_res[1].count_in + today_res[1].count_out

        if len(week_res) > 0:
            week_count = week_res[0].count_in + week_res[0].count_out

        if len(week_res) > 1:
            last_week_count = week_res[1].count_in + week_res[1].count_out

        crud.create_counter_summary(
            db, counter.identity, today, yesterday, week_count, last_week_count
        )

    return Response(status_code=status.HTTP_201_CREATED)
