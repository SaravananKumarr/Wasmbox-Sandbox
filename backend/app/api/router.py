from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.plugins import router as plugins_router
from app.api.execution import router as execution_router
from app.api.sandbox import router as sandbox_router

api_router = APIRouter()

api_router.include_router(
    health_router,
    tags=["Health"]
)

api_router.include_router(
    auth_router,
    tags=["Authentication"]
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
    sandbox_router,
    tags=["Sandbox"]
)