from fastapi import APIRouter
from pydantic import BaseModel

from app.sandbox.engine import execute_plugin

router = APIRouter()


class RunRequest(BaseModel):
    code: str
    input: str = "{}"


@router.post("/run")
def run_plugin(body: RunRequest):
    """Week 2 integration endpoint for the browser editor."""
    result = execute_plugin(body.code, body.input)
    return {
        "status": result["status"],
        "returnCode": result["return_code"],
        "duration": result["duration_ms"],
        "memory": result["memory_mb"],
        "output": result["output"],
        "logs": result["logs"],
    }
