from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PluginBase(BaseModel):
    name: str
    description: Optional[str] = None
    language: str = "python"
    source_code: str


class PluginCreate(PluginBase):
    pass


class PluginUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    source_code: Optional[str] = None
    status: Optional[str] = None


class PluginResponse(PluginBase):
    id: str
    wasm_path: Optional[str] = None
    status: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)