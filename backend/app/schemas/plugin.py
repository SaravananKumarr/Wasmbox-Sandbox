from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import DEFAULT_PLUGIN_CODE


# -------------------------------------
# Category & Tag Response
# -------------------------------------

class CategoryInfo(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class TagInfo(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


# -------------------------------------
# Base Plugin Schema
# -------------------------------------

class PluginBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = ""
    language: str = "python"

    # Keep both for compatibility
    code: str = DEFAULT_PLUGIN_CODE
    source_code: Optional[str] = None

    category_id: Optional[str] = None


# -------------------------------------
# Create Plugin
# -------------------------------------

class PluginCreate(PluginBase):
    pass


# -------------------------------------
# Import Existing WASM
# -------------------------------------

class PluginImport(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[str] = None


# -------------------------------------
# Update Plugin
# -------------------------------------

class PluginUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    language: Optional[str] = None

    code: Optional[str] = None
    source_code: Optional[str] = None

    status: Optional[str] = None
    category_id: Optional[str] = None


# -------------------------------------
# Plugin Response
# -------------------------------------

class PluginResponse(PluginBase):
    id: str

    wasm_path: Optional[str] = None
    status: str
    user_id: str

    created_at: datetime
    updated_at: datetime

    category: Optional[CategoryInfo] = None
    tags: list[TagInfo] = []

    model_config = ConfigDict(from_attributes=True)


# -------------------------------------
# Plugin List
# -------------------------------------

class PluginListResponse(BaseModel):
    page: int
    limit: int
    total: int
    pages: int

    items: list[PluginResponse]

    model_config = ConfigDict(from_attributes=True)


# -------------------------------------
# Search Query
# -------------------------------------

class PluginSearchQuery(BaseModel):
    page: int = 1
    limit: int = 10

    search: Optional[str] = None
    language: Optional[str] = None
    status: Optional[str] = None

    category: Optional[str] = None
    tag: Optional[str] = None

    sort: str = "created_at"
    order: str = "desc"

    @property
    def offset(self):
        return (self.page - 1) * self.limit