from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.schemas.plugin_share import (
    PluginShareCreate,
    PluginShareUpdate,
    PluginShareResponse,
)
from app.services.plugin_share_service import PluginShareService
from app.dependencies.current_user import get_current_user

router = APIRouter(
    prefix="/plugin-shares",
    tags=["Plugin Sharing"],
)


@router.post(
    "/{plugin_id}",
    response_model=PluginShareResponse,
    status_code=status.HTTP_201_CREATED,
)
def share_plugin(
    plugin_id: str,
    data: PluginShareCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return PluginShareService.share_plugin(
            db,
            plugin_id,
            data,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.get(
    "/{plugin_id}",
    response_model=list[PluginShareResponse],
)
def get_plugin_shares(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return PluginShareService.get_plugin_shares(
            db,
            plugin_id,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.put(
    "/{share_id}",
    response_model=PluginShareResponse,
)
def update_permission(
    share_id: str,
    data: PluginShareUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return PluginShareService.update_permission(
            db,
            share_id,
            data,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.delete(
    "/{share_id}",
)
def remove_share(
    share_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        PluginShareService.remove_share(
            db,
            share_id,
            current_user.id,
        )

        return {
            "message": "Plugin sharing removed successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.get(
    "/me/list",
    response_model=list[PluginShareResponse],
)
def shared_with_me(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PluginShareService.get_shared_with_me(
        db,
        current_user.id,
    )