import uuid

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.constants import DEFAULT_PLUGIN_CODE
from app.database.base import Base


class Plugin(Base):

    __tablename__ = "plugins"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=""
    )

    code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=DEFAULT_PLUGIN_CODE
    )

    language: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="python"
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Draft"
    )

    executions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    avg_runtime_ms: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
