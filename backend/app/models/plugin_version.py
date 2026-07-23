from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.plugin import Plugin


class PluginVersion(Base):
    __tablename__ = "plugin_versions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    plugin_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("plugins.id", ondelete="CASCADE"),
        nullable=False
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    source_code: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    wasm_path: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    plugin: Mapped["Plugin"] = relationship(
        back_populates="versions"
    )