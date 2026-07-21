from fastapi import APIRouter
from app.api.health import router as health_router
from app.routes.plugins import router as plugin_router
from app.routes.execution import router as execution_router
from app.routes.webhooks import router as webhook_router
from app.routes.auth import router as auth_router
from app.routes.websocket import router as ws_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(plugin_router, prefix="/api", tags=["Plugins"])
api_router.include_router(execution_router, prefix="/api", tags=["Execution"])
api_router.include_router(webhook_router, prefix="/api", tags=["Webhooks"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(ws_router)