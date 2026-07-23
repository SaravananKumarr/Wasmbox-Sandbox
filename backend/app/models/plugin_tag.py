import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PluginTag(Base):
    __tablename__ = "plugin_tags"

    __table_args__ = (
        UniqueConstraint(
            "plugin_id",
            "tag_id",
            name="uq_plugin_tag",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    plugin_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "plugins.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    tag_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "tags.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )