from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.schemas.execution import ExecuteRequest
from app.services import execution_service
from app.services import plugin_service

router = APIRouter()


@router.post("/execute")
def execute(data: ExecuteRequest, db: Session = Depends(get_db)):

    if data.plugin_id and plugin_service.get_plugin_model(db, data.plugin_id) is None:
        raise HTTPException(status_code=404, detail="Plugin not found")

    return execution_service.run_execution(
        db,
        code=data.code,
        input_payload=data.input,
        plugin_id=data.plugin_id,
    )


@router.get("/executions/history")
def execution_history(limit: int = 50, db: Session = Depends(get_db)):

    return execution_service.get_history(db, limit=limit)


@router.get("/metrics/summary")
def metrics_summary(db: Session = Depends(get_db)):

    return execution_service.get_metrics_summary(db)
