from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class PluginShareCreate(BaseModel):
    user_id: str
    permission: Literal["view", "edit"] = "view"


class PluginShareUpdate(BaseModel):
    permission: Literal["view", "edit"]


class PluginShareResponse(BaseModel):
    id: str
    plugin_id: str
    user_id: str
    permission: str
    shared_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )