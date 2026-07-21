from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.schemas.execution import ExecutionResponse
from app.services.execution_service import execution_service
from app.services.plugin_service import plugin_service

router = APIRouter(
    prefix="/executions",
    tags=["Executions"],
)


@router.post(
    "/{plugin_id}",
    response_model=ExecutionResponse,
)
def execute_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    plugin = plugin_service.get_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )

    return execution_service.execute_plugin(
        db=db,
        plugin=plugin,
    )


@router.get(
    "/history/{plugin_id}",
    response_model=list[ExecutionResponse],
)
def execution_history(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    plugin = plugin_service.get_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )

    return execution_service.get_history(
        db=db,
        plugin_id=plugin.id,
    )