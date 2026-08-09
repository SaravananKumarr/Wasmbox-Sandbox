from fastapi import APIRouter
from pydantic import BaseModel

from app.sandbox.engine import execute_plugin

router = APIRouter()


class RunRequest(BaseModel):
    code: str
    input: str = "{}"


@router.post("/run")
def run_plugin(body: RunRequest):
    """Execute source code and return a consistent execution result."""
    result = execute_plugin(body.code, body.input)
    return {
        "status": result["status"],
        "return_code": result["return_code"],
        "duration_ms": result["duration_ms"],
        "memory_mb": result["memory_mb"],
        "output": result["output"],
        "error_message": result["error_message"],
        "logs": result["logs"],
    }
