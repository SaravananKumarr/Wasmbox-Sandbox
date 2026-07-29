from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.plugins import router as plugins_router
from app.core.constants import API_PREFIX

api_router = APIRouter(prefix=API_PREFIX)

api_router.include_router(
    health_router,
    tags=["Health"]
)

api_router.include_router(auth_router)

api_router.include_router(plugins_router)