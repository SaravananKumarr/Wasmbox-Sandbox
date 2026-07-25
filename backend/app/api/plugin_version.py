from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.schemas.plugin_version import (
    PluginVersionCreate,
    PluginVersionResponse,
    PluginVersionUpdate,
)
from app.services.plugin_service import plugin_service
from app.services.plugin_version_service import PluginVersionService

router = APIRouter(
    prefix="/plugins",
    tags=["Plugin Versions"],
)


@router.post(
    "/{plugin_id}/versions",
    response_model=PluginVersionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_version(
    plugin_id: str,
    data: PluginVersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plugin = plugin_service.get_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )

    return PluginVersionService.create_version(
        db=db,
        plugin=plugin,
        data=data,
    )


@router.get(
    "/{plugin_id}/versions",
    response_model=list[PluginVersionResponse],
)
def get_versions(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plugin_service.get_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )

    return PluginVersionService.get_versions(
        db=db,
        plugin_id=plugin_id,
    )


@router.get(
    "/{plugin_id}/versions/latest",
    response_model=PluginVersionResponse,
)
def get_latest_version(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plugin_service.get_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )

    return PluginVersionService.get_latest_version(
        db=db,
        plugin_id=plugin_id,
    )


@router.put(
    "/versions/{version_id}",
    response_model=PluginVersionResponse,
)
def update_version(
    version_id: str,
    data: PluginVersionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PluginVersionService.update_version(
        db=db,
        version_id=version_id,
        data=data,
    )


@router.delete(
    "/versions/{version_id}",
)
def delete_version(
    version_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PluginVersionService.delete_version(
        db=db,
        version_id=version_id,
    )


@router.post(
    "/{plugin_id}/versions/{version_id}/rollback",
    response_model=PluginVersionResponse,
)
def rollback_version(
    plugin_id: str,
    version_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plugin = plugin_service.get_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )

    return PluginVersionService.restore_version(
        db=db,
        plugin=plugin,
        version_id=version_id,
    )