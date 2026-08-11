from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings
from app.sandbox.engine import execute_plugin

router = APIRouter()


class RunRequest(BaseModel):
    code: str
    input: str = "{}"


@router.post("/run")
def run_plugin(body: RunRequest):
    """Execute source code and return a consistent execution result."""
    result = execute_plugin(body.code, body.input)
    resource_usage = {
        "duration_ms": result["duration_ms"],
        "memory_mb": result["memory_mb"],
        # Python-source execution does not yet traverse the Wasmtime runtime.
        # This becomes a number when a compiled Wasm module is run.
        "fuel_consumed": result.get("fuel_consumed"),
    }
    return {
        "status": result["status"],
        "return_code": result["return_code"],
        "duration_ms": result["duration_ms"],
        "memory_mb": result["memory_mb"],
        "output": result["output"],
        "error_message": result["error_message"],
        "logs": result["logs"],
        "resource_usage": resource_usage,
        "resource_limits": {
            "execution_timeout_ms": int(settings.SANDBOX_TIMEOUT_SECONDS * 1000),
            "sandbox_memory_mb": settings.SANDBOX_MEMORY_MB,
            "wasm_memory_mb": settings.WASM_MEMORY_LIMIT_MB,
            "wasm_fuel": settings.WASM_FUEL_LIMIT,
        },
    }
