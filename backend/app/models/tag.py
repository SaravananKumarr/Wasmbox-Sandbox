import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.plugin_tag import PluginTag

if TYPE_CHECKING:
    from app.models.plugin import Plugin


class Tag(Base):
    __tablename__ = "tags"

    # =========================
    # Primary Key
    # =========================
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # =========================
    # Tag Name
    # =========================
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    # =========================
    # Relationships
    # =========================
    plugins: Mapped[list["Plugin"]] = relationship(
        "Plugin",
        secondary=PluginTag.__table__,
        back_populates="tags",
    )