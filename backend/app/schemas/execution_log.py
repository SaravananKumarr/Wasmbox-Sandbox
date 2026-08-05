from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ExecutionLogFilter(BaseModel):
    page: int = 1
    limit: int = 10
    status: Literal["success", "failed"] | None = None


class ExecutionLogResponse(BaseModel):
    id: str
    plugin_id: str

    status: str

    stdout: str | None = None
    stderr: str | None = None

    exit_code: int
    duration: float
    memory_used: int | None = None

    executed_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ExecutionLogListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[ExecutionLogResponse]