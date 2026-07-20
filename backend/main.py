from fastapi import FastAPI

from app.api.router import api_router
from app.core.constants import APP_NAME

app = FastAPI(
    title=APP_NAME,
    version="1.0.0"
)

app.include_router(api_router)


@app.get("/")
def root():

    return {
        "message": "Welcome to WasmBox Sandbox"
    }