from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class MarketplacePlugin(Base):
    __tablename__ = "marketplace_plugins"

    # Primary Key
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    # Foreign Key -> plugins.id (VARCHAR(36))
    plugin_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("plugins.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    downloads: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    views: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    published_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    plugin = relationship(
        "Plugin",
        back_populates="marketplace",
    )