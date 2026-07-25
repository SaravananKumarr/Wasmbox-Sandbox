import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.plugin import Plugin


class Collection(Base):
    __tablename__ = "collections"

    # ---------------------------------
    # Primary Key
    # ---------------------------------

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # ---------------------------------
    # Owner
    # ---------------------------------

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ---------------------------------
    # Collection Name
    # ---------------------------------

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # ---------------------------------
    # Description
    # ---------------------------------

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------
    # Public / Private
    # ---------------------------------

    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ---------------------------------
    # Featured Collection
    # ---------------------------------

    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ---------------------------------
    # Created At
    # ---------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # ---------------------------------
    # Updated At
    # ---------------------------------

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="collections",
    )

    plugins: Mapped[list["Plugin"]] = relationship(
        "Plugin",
        secondary="collection_plugins",
        back_populates="collections",
    )