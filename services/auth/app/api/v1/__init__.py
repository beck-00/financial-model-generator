from fastapi import APIRouter

api_router = APIRouter()

from .endpoints import auth
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])