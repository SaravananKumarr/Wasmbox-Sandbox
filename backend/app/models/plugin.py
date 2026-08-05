import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
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
    from app.models.user import User
    from app.models.execution import Execution
    from app.models.plugin_version import PluginVersion
    from app.models.review import Review
    from app.models.favorite import Favorite
    from app.models.comment import Comment
    from app.models.category import Category
    from app.models.tag import Tag
    from app.models.collection import Collection
    from app.models.plugin_share import PluginShare
    from app.models.execution_log import ExecutionLog
    from app.models.marketplace import MarketplacePlugin
    from app.models.plugin_install import PluginInstall


class Plugin(Base):
    __tablename__ = "plugins"

    # =====================================================
    # Primary Key
    # =====================================================

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    # =====================================================
    # Plugin Information
    # =====================================================

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    language: Mapped[str] = mapped_column(
        String(20),
        default="python",
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
        default="draft",
    )

    # =====================================================
    # Foreign Keys
    # =====================================================

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    category_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )

    # =====================================================
    # Timestamps
    # =====================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # =====================================================
    # Relationships
    # =====================================================

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="plugins",
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="plugins",
    )

    executions: Mapped[list["Execution"]] = relationship(
        "Execution",
        back_populates="plugin",
        cascade="all, delete-orphan",
    )

    versions: Mapped[list["PluginVersion"]] = relationship(
        "PluginVersion",
        back_populates="plugin",
        cascade="all, delete-orphan",
        order_by="PluginVersion.version",
    )

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="plugin",
        cascade="all, delete-orphan",
    )

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite",
        back_populates="plugin",
        cascade="all, delete-orphan",
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="plugin",
        cascade="all, delete-orphan",
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="plugin_tags",
        back_populates="plugins",
    )

    collections: Mapped[list["Collection"]] = relationship(
        "Collection",
        secondary="collection_plugins",
        back_populates="plugins",
    )

    installs: Mapped[list["PluginInstall"]] = relationship(
        "PluginInstall",
        back_populates="plugin",
        cascade="all, delete-orphan",
    )

    shares: Mapped[list["PluginShare"]] = relationship(
        "PluginShare",
        back_populates="plugin",
        cascade="all, delete-orphan",
    )

    execution_logs: Mapped[list["ExecutionLog"]] = relationship(
        "ExecutionLog",
        back_populates="plugin",
        cascade="all, delete-orphan",
        order_by="ExecutionLog.executed_at.desc()",
    )

    marketplace: Mapped["MarketplacePlugin | None"] = relationship(
        "MarketplacePlugin",
        back_populates="plugin",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self) -> str:
        return (
            f"<Plugin("
            f"id='{self.id}', "
            f"name='{self.name}', "
            f"status='{self.status}'"
            f")>"
        )