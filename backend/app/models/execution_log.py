import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
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
    from app.models.plugin import Plugin


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    plugin_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("plugins.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    plugin_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="draft",
    )

    code: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    input_payload: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="{}",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    stdout: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    stderr: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    output: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    exit_code: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    return_code: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    duration: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    duration_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    memory_used: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    memory_mb: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    logs: Mapped[list] = mapped_column(
        JSON,
        default=list,
    )

    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    plugin: Mapped["Plugin"] = relationship(
        "Plugin",
        back_populates="execution_logs",
    )