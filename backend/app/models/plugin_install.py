import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base


class PluginInstall(Base):
    __tablename__ = "plugin_installs"

    __table_args__ = (
        UniqueConstraint(
            "plugin_id",
            "user_id",
            name="uq_plugin_install",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    plugin_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "plugins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    installed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    plugin = relationship(
        "Plugin",
        back_populates="installs",
    )

    user = relationship(
        "User",
        back_populates="installed_plugins",
    )