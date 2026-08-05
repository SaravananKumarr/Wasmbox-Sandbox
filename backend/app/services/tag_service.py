from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.plugin_repository import plugin_repository
from app.repositories.tag_repository import tag_repository

from app.schemas.tag import (
    TagCreate,
    TagUpdate,
)


class TagService:
    """
    Business logic for Tag operations.
    """

    # -------------------------------------
    # Create Tag
    # -------------------------------------

    def create_tag(
        self,
        db: Session,
        tag: TagCreate,
    ):

        existing = tag_repository.get_tag_by_name(
            db=db,
            name=tag.name,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag already exists.",
            )

        return tag_repository.create_tag(
            db=db,
            tag=tag,
        )

    # -------------------------------------
    # Get Tags
    # -------------------------------------

    def get_tags(
        self,
        db: Session,
    ):

        return tag_repository.get_tags(db)

    # -------------------------------------
    # Update Tag
    # -------------------------------------

    def update_tag(
        self,
        db: Session,
        tag_id: str,
        tag: TagUpdate,
    ):

        db_tag = tag_repository.get_tag(
            db=db,
            tag_id=tag_id,
        )

        if db_tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found.",
            )

        return tag_repository.update_tag(
            db=db,
            db_tag=db_tag,
            tag=tag,
        )

    # -------------------------------------
    # Delete Tag
    # -------------------------------------

    def delete_tag(
        self,
        db: Session,
        tag_id: str,
    ):

        db_tag = tag_repository.get_tag(
            db=db,
            tag_id=tag_id,
        )

        if db_tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found.",
            )

        tag_repository.delete_tag(
            db=db,
            db_tag=db_tag,
        )

        return {
            "message": "Tag deleted successfully."
        }

    # -------------------------------------
    # Assign Tag
    # -------------------------------------

    def assign_tag(
        self,
        db: Session,
        plugin_id: str,
        tag_id: str,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        tag = tag_repository.get_tag(
            db=db,
            tag_id=tag_id,
        )

        if tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found.",
            )

        return tag_repository.assign_tag(
            db=db,
            plugin=plugin,
            tag=tag,
        )

    # -------------------------------------
    # Remove Tag
    # -------------------------------------

    def remove_tag(
        self,
        db: Session,
        plugin_id: str,
        tag_id: str,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        tag = tag_repository.get_tag(
            db=db,
            tag_id=tag_id,
        )

        if tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found.",
            )

        return tag_repository.remove_tag(
            db=db,
            plugin=plugin,
            tag=tag,
        )

    # -------------------------------------
    # Plugin Tags
    # -------------------------------------

    def get_plugin_tags(
        self,
        db: Session,
        plugin_id: str,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        return tag_repository.get_plugin_tags(plugin)


tag_service = TagService()