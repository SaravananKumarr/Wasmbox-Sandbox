from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.schemas.plugin_version import PluginVersionResponse
from app.services.plugin_service import plugin_service
from app.services.plugin_version_service import PluginVersionService

router = APIRouter(
    prefix="/plugins",
    tags=["Plugin Versions"],
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
    # Verify plugin ownership
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
    "/{plugin_id}/versions/{version}",
    response_model=PluginVersionResponse,
)
def get_version(
    plugin_id: str,
    version: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify plugin ownership
    plugin_service.get_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )

    plugin_version = PluginVersionService.get_version(
        db=db,
        plugin_id=plugin_id,
        version=version,
    )

    if plugin_version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plugin version not found",
        )

    return plugin_version


@router.post(
    "/{plugin_id}/versions/{version}/restore",
    status_code=status.HTTP_200_OK,
)
def restore_plugin_version(
    plugin_id: str,
    version: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify plugin ownership
    plugin = plugin_service.get_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )

    restored_plugin = PluginVersionService.restore_version(
        db=db,
        plugin=plugin,
        version=version,
    )

    if restored_plugin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plugin version not found",
        )

    return {
        "message": f"Plugin restored successfully to version {version}",
        "plugin_id": restored_plugin.id,
        "current_version": PluginVersionService.get_versions(
            db=db,
            plugin_id=plugin.id,
        )[0].version,
    }