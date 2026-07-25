import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
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
        index=True,
    )

    # ---------------------------------
    # Execution Status
    # ---------------------------------

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    # ---------------------------------
    # Standard Output
    # ---------------------------------

    stdout: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------
    # Standard Error
    # ---------------------------------

    stderr: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------
    # Exit Code
    # ---------------------------------

    exit_code: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ---------------------------------
    # Execution Duration (Seconds)
    # ---------------------------------

    duration: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    # ---------------------------------
    # Memory Used (KB)
    # ---------------------------------

    memory_used: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # ---------------------------------
    # Executed At
    # ---------------------------------

    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ---------------------------------
    # Relationship
    # ---------------------------------

    plugin: Mapped["Plugin"] = relationship(
        "Plugin",
        back_populates="execution_logs",
    )