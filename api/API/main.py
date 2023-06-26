from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from . import config, models
from .db import engine
from .routers import admin, counts

models.Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/api", title="WMCycleCounter")
app.add_middleware(SessionMiddleware, secret_key=config.SessionSecret)

app.include_router(counts.router)
app.include_router(admin.router)
