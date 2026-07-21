from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PluginBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    source_code: str = Field(..., min_length=1)


class PluginCreate(PluginBase):
    owner: str = Field(..., min_length=1, max_length=255)
    is_public: bool = False


class PluginUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    source_code: Optional[str] = Field(None, min_length=1)
    is_public: Optional[bool] = None


class PluginOut(PluginBase):
    id: str
    owner: str
    wasm_binary: Optional[bytes] = None
    is_public: bool
    execution_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class PluginList(BaseModel):
    plugins: List[PluginOut]


class ExecutionLogBase(BaseModel):
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    execution_time_ms: Optional[float] = None
    memory_bytes: Optional[int] = None
    fuel_consumed: Optional[int] = None
    status: str


class ExecutionLogCreate(ExecutionLogBase):
    plugin_id: str


class ExecutionLogOut(ExecutionLogBase):
    id: str
    plugin_id: str
    executed_at: datetime

    model_config = {
        "from_attributes": True
    }
