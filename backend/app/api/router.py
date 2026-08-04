from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.plugins import router as plugins_router
from app.api.execution import router as execution_router
from app.api.security import router as security_router
from app.api.runtime import router as runtime_router

api_router = APIRouter()

api_router.include_router(
    health_router,
    tags=["Health"]
)

api_router.include_router(
    plugins_router,
    tags=["Plugins"]
)

api_router.include_router(
    execution_router,
    tags=["Execution"]
)

api_router.include_router(
    security_router,
    tags=["Security"]
)

api_router.include_router(
    runtime_router,
    tags=["Runtime"]
)
