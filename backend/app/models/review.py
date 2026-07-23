import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Review(Base):
    __tablename__ = "reviews"

    __table_args__ = (
        UniqueConstraint(
            "plugin_id",
            "user_id",
            name="uq_plugin_review",
        ),
    )

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    plugin_id: Mapped[str] = mapped_column(
        ForeignKey("plugins.id", ondelete="CASCADE"),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    plugin = relationship("Plugin")
    user = relationship("User")