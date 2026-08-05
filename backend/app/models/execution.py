import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Execution(Base):
    __tablename__ = "executions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    plugin_id: Mapped[str] = mapped_column(
        ForeignKey("plugins.id", ondelete="CASCADE"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="SUCCESS",
        nullable=False,
    )

    output: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    error: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    execution_time: Mapped[str] = mapped_column(
        String(20),
        default="0 ms",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    plugin = relationship(
        "Plugin",
        back_populates="executions",
    )