from fastapi import APIRouter

from app.api.execution import router as execution_router
from app.api.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(execution_router, tags=["Execution"])
