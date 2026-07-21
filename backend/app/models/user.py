import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.plugin import Plugin


class User(Base):
    __tablename__ = "users"

    # Primary Key (UUID)
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    # Username
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    # Email
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    # Hashed Password
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Account Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Created Time
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationship with Plugins
    plugins: Mapped[list["Plugin"]] = relationship(
        "Plugin",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"username='{self.username}', "
            f"email='{self.email}')>"
        )