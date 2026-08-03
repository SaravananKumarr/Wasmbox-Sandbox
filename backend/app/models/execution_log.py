import uuid

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class ExecutionLog(Base):

    __tablename__ = "execution_logs"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    plugin_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("plugins.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    plugin_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="draft"
    )

    code: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    input_payload: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="{}"
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    return_code: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    duration_ms: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )

    memory_mb: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )

    output: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    logs: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list
    )

    error_message: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )
