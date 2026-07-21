import uuid
from sqlalchemy import Boolean, DateTime, String, Text, LargeBinary, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database.base import Base


class Plugin(Base):
    __tablename__ = "plugins"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    source_code: Mapped[str] = mapped_column(Text, nullable=False)
    wasm_binary: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    execution_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    execution_logs = relationship("ExecutionLog", back_populates="plugin", cascade="all, delete-orphan")


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    plugin_id: Mapped[str] = mapped_column(String, ForeignKey("plugins.id"), nullable=False)
    stdout: Mapped[str] = mapped_column(Text, nullable=True)
    stderr: Mapped[str] = mapped_column(Text, nullable=True)
    execution_time_ms: Mapped[float] = mapped_column(Float, nullable=True)
    memory_bytes: Mapped[int] = mapped_column(Integer, nullable=True)
    fuel_consumed: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    executed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    plugin = relationship("Plugin", back_populates="execution_logs")
