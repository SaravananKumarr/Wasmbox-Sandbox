from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.schemas.plugin import (
    PluginCreate,
    PluginUpdate,
    PluginResponse,
)
from app.services.plugin_service import plugin_service

router = APIRouter(
    prefix="/plugins",
    tags=["Plugins"],
)


@router.post(
    "/",
    response_model=PluginResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_plugin(
    plugin: PluginCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return plugin_service.create_plugin(
        db=db,
        plugin=plugin,
        user_id=current_user.id,
    )


@router.get(
    "/",
    response_model=list[PluginResponse],
)
def get_plugins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return plugin_service.get_plugins(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{plugin_id}",
    response_model=PluginResponse,
)
def get_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return plugin_service.get_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )


@router.put(
    "/{plugin_id}",
    response_model=PluginResponse,
)
def update_plugin(
    plugin_id: str,
    plugin: PluginUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return plugin_service.update_plugin(
        db=db,
        plugin_id=plugin_id,
        plugin_data=plugin,
        user_id=current_user.id,
    )


@router.delete(
    "/{plugin_id}",
)
def delete_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return plugin_service.delete_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )