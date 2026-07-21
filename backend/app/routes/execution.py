from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.plugin import Plugin
from app.utils.response import success, error
from app.services.execution_service import ExecutionService

class RunRequest(BaseModel):
    source_code: str
    owner: str = "anonymous"

router = APIRouter()


@router.post("/run", response_model=dict)
def run_plugin(req: RunRequest, db: Session = Depends(get_db)):
    service = ExecutionService(db)
    result = service.run_from_source(req.source_code, req.owner)
    if result.get("status") == "error":
        return error(result.get("message", "Execution failed"))
    return success("Execution completed", result)


@router.post("/trigger/{plugin_id}", response_model=dict)
def trigger_plugin(plugin_id: str, db: Session = Depends(get_db)):
    service = ExecutionService(db)
    result = service.trigger_by_id(plugin_id)
    if result.get("status") == "error":
        return error(result.get("message", "Trigger failed"))
    return success("Trigger completed", result)
