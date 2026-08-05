from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependency import get_db

from app.schemas.tag import (
    TagCreate,
    TagUpdate,
    TagResponse,
)

from app.schemas.plugin_tag import PluginTagCreate

from app.services.tag_service import tag_service

router = APIRouter(
    tags=["Tags"],
)


# =====================================
# Tag CRUD
# =====================================

@router.post(
    "/tags",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db),
):
    return tag_service.create_tag(db, tag)


@router.get(
    "/tags",
    response_model=list[TagResponse],
)
def get_tags(
    db: Session = Depends(get_db),
):
    return tag_service.get_tags(db)


@router.put(
    "/tags/{tag_id}",
    response_model=TagResponse,
)
def update_tag(
    tag_id: str,
    tag: TagUpdate,
    db: Session = Depends(get_db),
):
    return tag_service.update_tag(
        db,
        tag_id,
        tag,
    )


@router.delete(
    "/tags/{tag_id}",
)
def delete_tag(
    tag_id: str,
    db: Session = Depends(get_db),
):
    return tag_service.delete_tag(
        db,
        tag_id,
    )


# =====================================
# Plugin Tags
# =====================================

@router.post(
    "/plugins/{plugin_id}/tags",
)
def assign_tag(
    plugin_id: str,
    request: PluginTagCreate,
    db: Session = Depends(get_db),
):
    return tag_service.assign_tag(
        db,
        plugin_id,
        request.tag_id,
    )


@router.delete(
    "/plugins/{plugin_id}/tags/{tag_id}",
)
def remove_tag(
    plugin_id: str,
    tag_id: str,
    db: Session = Depends(get_db),
):
    return tag_service.remove_tag(
        db,
        plugin_id,
        tag_id,
    )


@router.get(
    "/plugins/{plugin_id}/tags",
    response_model=list[TagResponse],
)
def get_plugin_tags(
    plugin_id: str,
    db: Session = Depends(get_db),
):
    return tag_service.get_plugin_tags(
        db,
        plugin_id,
    )