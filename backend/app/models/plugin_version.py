from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.plugin import Plugin


class PluginVersion(Base):
    __tablename__ = "plugin_versions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    plugin_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("plugins.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Semantic Version
    # Examples:
    # 1.0.0
    # 1.1.0
    # 2.0.0
    version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    title: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    changelog: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    release_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source_code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    wasm_path: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="stable",
        nullable=False,
    )

    is_latest: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    plugin: Mapped["Plugin"] = relationship(
        "Plugin",
        back_populates="versions",
    )