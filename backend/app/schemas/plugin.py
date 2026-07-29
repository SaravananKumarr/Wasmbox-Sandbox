from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class PluginOut(BaseModel):

    id: str

    name: str

    description: Optional[str]

    filename: str

    version: str

    owner_id: str

    is_active: bool

    created_at: datetime

    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class PluginUpdate(BaseModel):

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)

    description: Optional[str] = Field(default=None, max_length=500)

    is_active: Optional[bool] = None


class ExecuteRequest(BaseModel):

    # Name of an exported function to call directly. If omitted, the
    # module's WASI "_start" entrypoint is run instead.
    function: Optional[str] = None

    args: list[float | int] = []

    # Text piped to stdin when running in WASI mode.
    stdin: Optional[str] = None


class ExecuteResponse(BaseModel):

    success: bool

    mode: str

    return_value: Optional[Any] = None

    stdout: Optional[str] = None

    stderr: Optional[str] = None

    error: Optional[str] = None

    execution_time_ms: float

    fuel_consumed: Optional[int] = None
