from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.openapi.utils import get_openapi

from . import config
# from .routers import report,crossings

app = FastAPI(root_path="/api",title="WMCycleCounter")
print("starting")
app.add_middleware(SessionMiddleware, secret_key=config.SessionSecret)
# openapi_schema = get_openapi(title="BadlyParked",version="1.0.0",routes=app.routes,description="This is a very custom OpenAPI schema")
# app.openapi_schema = openapi_schema
# app.openapi = app.openapi_schema
# app.include_router(uploads.router)
# app.include_router(report.router)
# app.include_router(crossings.router)