import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.collection import Collection
    from app.models.plugin import Plugin


class CollectionPlugin(Base):
    __tablename__ = "collection_plugins"

    __table_args__ = (
        UniqueConstraint(
            "collection_id",
            "plugin_id",
            name="uq_collection_plugin",
        ),
    )

    # ---------------------------------
    # Primary Key
    # ---------------------------------

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # ---------------------------------
    # Collection ID
    # ---------------------------------

    collection_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "collections.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ---------------------------------
    # Plugin ID
    # ---------------------------------

    plugin_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "plugins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ---------------------------------
    # Added At
    # ---------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    collection: Mapped["Collection"] = relationship(
        "Collection",
        back_populates="plugins",
    )

    plugin: Mapped["Plugin"] = relationship(
        "Plugin",
        back_populates="collections",
    )