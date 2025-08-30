from .core.config import settings
from fastapi import FastAPI
from .api.v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)