from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from app.core.constants import DEFAULT_PLUGIN_CODE


class PluginCreate(BaseModel):

    name: str = Field(..., min_length=1, max_length=255)

    description: str = ""

    code: str = DEFAULT_PLUGIN_CODE

    language: str = "python"


class PluginUpdate(BaseModel):

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)

    description: Optional[str] = None

    code: Optional[str] = None

    status: Optional[str] = None
