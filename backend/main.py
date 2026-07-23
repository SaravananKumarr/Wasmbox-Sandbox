from fastapi import FastAPI

from app.api.router import api_router
from app.api.plugin import router as plugin_router
from app.api.execution import router as execution_router
from app.api.plugin_version import router as plugin_version_router
from app.core.constants import APP_NAME
from app.api.review import router as review_router
from app.api.favorite import router as favorite_router
from app.api.category import router as category_router
from app.api.tag import router as tag_router

app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
)

app.include_router(api_router)
app.include_router(plugin_router)
app.include_router(execution_router)
app.include_router(plugin_version_router)
app.include_router(review_router)
app.include_router(favorite_router)
app.include_router(category_router)
app.include_router(tag_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to WasmBox Sandbox"
    }