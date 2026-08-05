from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.schemas.plugin_install import (
    PluginInstallListResponse,
    PluginInstallResponse,
)
from app.services.plugin_install_service import PluginInstallService

router = APIRouter(
    prefix="/plugin-installs",
    tags=["Plugin Installation"],
)


@router.post(
    "/{plugin_id}",
    response_model=PluginInstallResponse,
)
def install_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return PluginInstallService.install_plugin(
            db,
            plugin_id,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete("/{plugin_id}")
def uninstall_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        PluginInstallService.uninstall_plugin(
            db,
            plugin_id,
            current_user.id,
        )

        return {
            "message": "Plugin uninstalled successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.get(
    "/me",
    response_model=PluginInstallListResponse,
)
def my_installed_plugins(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PluginInstallService.get_my_plugins(
        db,
        current_user.id,
        page,
        limit,
    )


@router.get("/{plugin_id}/count")
def installation_count(
    plugin_id: str,
    db: Session = Depends(get_db),
):
    return {
        "plugin_id": plugin_id,
        "installations": PluginInstallService.installation_count(
            db,
            plugin_id,
        ),
    }