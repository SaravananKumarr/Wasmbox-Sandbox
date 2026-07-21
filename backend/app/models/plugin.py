import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Plugin(Base):
    __tablename__ = "plugins"

    # Primary Key (UUID)
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    # Plugin Name
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Description
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Programming Language
    language: Mapped[str] = mapped_column(
        String(20),
        default="python",
    )

    # Source Code
    source_code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Compiled WASM Path
    wasm_path: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
    )

    # User UUID
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Created At
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Updated At
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship
    owner = relationship(
        "User",
        back_populates="plugins",
    )

    executions = relationship(
    "Execution",
    back_populates="plugin",
    cascade="all, delete-orphan",
)