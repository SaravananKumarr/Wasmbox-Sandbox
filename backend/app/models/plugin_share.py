import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.plugin import Plugin
    from app.models.user import User


class PluginShare(Base):
    __tablename__ = "plugin_shares"

    __table_args__ = (
        UniqueConstraint(
            "plugin_id",
            "user_id",
            name="uq_plugin_share",
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
    # Plugin
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
    # Shared User
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
    # Permission
    # ---------------------------------

    permission: Mapped[str] = mapped_column(
        String(10),
        default="view",
        nullable=False,
    )

    # ---------------------------------
    # Shared At
    # ---------------------------------

    shared_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    plugin: Mapped["Plugin"] = relationship(
        "Plugin",
        back_populates="shares",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="shared_plugins",
    )