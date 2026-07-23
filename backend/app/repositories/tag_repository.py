from sqlalchemy.orm import Session

from app.models.plugin import Plugin
from app.models.tag import Tag
from app.schemas.tag import (
    TagCreate,
    TagUpdate,
)


class TagRepository:
    """
    Repository for Tag database operations.
    """

    # -------------------------------------
    # Create Tag
    # -------------------------------------

    def create_tag(
        self,
        db: Session,
        tag: TagCreate,
    ) -> Tag:

        db_tag = Tag(
            name=tag.name,
        )

        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)

        return db_tag

    # -------------------------------------
    # Get Tag
    # -------------------------------------

    def get_tag(
        self,
        db: Session,
        tag_id: str,
    ) -> Tag | None:

        return (
            db.query(Tag)
            .filter(Tag.id == tag_id)
            .first()
        )

    # -------------------------------------
    # Get Tag By Name
    # -------------------------------------

    def get_tag_by_name(
        self,
        db: Session,
        name: str,
    ) -> Tag | None:

        return (
            db.query(Tag)
            .filter(Tag.name == name)
            .first()
        )

    # -------------------------------------
    # Get All Tags
    # -------------------------------------

    def get_tags(
        self,
        db: Session,
    ):

        return (
            db.query(Tag)
            .order_by(Tag.name.asc())
            .all()
        )

    # -------------------------------------
    # Update Tag
    # -------------------------------------

    def update_tag(
        self,
        db: Session,
        db_tag: Tag,
        tag: TagUpdate,
    ) -> Tag:

        update_data = tag.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(db_tag, key, value)

        db.commit()
        db.refresh(db_tag)

        return db_tag

    # -------------------------------------
    # Delete Tag
    # -------------------------------------

    def delete_tag(
        self,
        db: Session,
        db_tag: Tag,
    ):

        db.delete(db_tag)
        db.commit()

    # -------------------------------------
    # Assign Tag To Plugin
    # -------------------------------------

    def assign_tag(
        self,
        db: Session,
        plugin: Plugin,
        tag: Tag,
    ):

        if tag not in plugin.tags:
            plugin.tags.append(tag)
            db.commit()
            db.refresh(plugin)

        return plugin

    # -------------------------------------
    # Remove Tag
    # -------------------------------------

    def remove_tag(
        self,
        db: Session,
        plugin: Plugin,
        tag: Tag,
    ):

        if tag in plugin.tags:
            plugin.tags.remove(tag)
            db.commit()
            db.refresh(plugin)

        return plugin

    # -------------------------------------
    # Get Plugin Tags
    # -------------------------------------

    def get_plugin_tags(
        self,
        plugin: Plugin,
    ):

        return plugin.tags


tag_repository = TagRepository()