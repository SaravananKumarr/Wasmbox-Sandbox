from fastapi import FastAPI

# ==========================
# Database Initialization
# ==========================
from app.database.base import Base
from app.database.connection import engine

# Import all models so SQLAlchemy registers them
import app.models

# Create all tables if they don't exist
Base.metadata.create_all(bind=engine)

# ==========================
# API Routers
# ==========================
from app.api.router import api_router
from app.api.plugin import router as plugin_router
from app.api.execution import router as execution_router
from app.api.plugin_version import router as plugin_version_router
from app.api.review import router as review_router
from app.api.favorite import router as favorite_router
from app.api.category import router as category_router
from app.api.tag import router as tag_router
from app.api.collection import router as collection_router
from app.api.plugin_share import router as plugin_share_router
from app.api.execution_log import router as execution_log_router
from app.api.marketplace import router as marketplace_router
from app.api.plugin_install import router as plugin_install_router

from app.core.constants import APP_NAME
from app.api import plugin_version
from app.api.comment import router as comment_router
from app.api.analytics import router as analytics_router

# ==========================
# FastAPI App
# ==========================
app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
)

# ==========================
# Register Routers
# ==========================
app.include_router(api_router)
app.include_router(plugin_router)
app.include_router(execution_router)
app.include_router(plugin_version_router)
app.include_router(review_router)
app.include_router(favorite_router)
app.include_router(category_router)
app.include_router(tag_router)
app.include_router(collection_router)
app.include_router(plugin_share_router)
app.include_router(execution_log_router)
app.include_router(marketplace_router)
app.include_router(plugin_install_router)
app.include_router(comment_router)
app.include_router(analytics_router)

# ==========================
# Root Endpoint
# ==========================
@app.get("/")
def root():
    return {
        "message": "Welcome to WasmBox Sandbox"
    }