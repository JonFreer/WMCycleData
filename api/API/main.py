from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from . import config, models, scheduler
from .db import engine
from .db_init import init_timescale
from .routers import admin, counts

models.Base.metadata.create_all(
    bind=engine,
    tables=[
        table
        for table in models.Base.metadata.sorted_tables
        if table not in models.CONTINUOUS_AGGREGATES
    ],
)
init_timescale(engine)

if config.SchedulerEnabled:
    scheduler.start()

app = FastAPI(root_path="/api", title="WMCycleCounter")
app.add_middleware(SessionMiddleware, secret_key=config.SessionSecret)

app.include_router(counts.router)
app.include_router(admin.router)
