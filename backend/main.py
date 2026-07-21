from fastapi import FastAPI

from app.api.router import api_router
from app.api.plugin import router as plugin_router
from app.core.constants import APP_NAME

from app.api.execution import router as execution_router

app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
)

app.include_router(api_router)
app.include_router(plugin_router)
app.include_router(execution_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to WasmBox Sandbox"
    }