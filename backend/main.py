import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.constants import APP_NAME

os.makedirs(settings.PLUGIN_STORAGE_DIR, exist_ok=True)

app = FastAPI(
    title=APP_NAME,
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router)


@app.get("/")
def root():

    return {
        "message": "Welcome to WasmBox Sandbox"
    }