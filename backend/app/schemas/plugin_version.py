from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PluginVersionBase(BaseModel):
    version: str
    source_code: str
    wasm_path: str | None = None
    title: str | None = None
    changelog: str | None = None
    release_notes: str | None = None
    status: str = "stable"


class PluginVersionCreate(PluginVersionBase):
    pass


class PluginVersionUpdate(BaseModel):
    title: str | None = None
    changelog: str | None = None
    release_notes: str | None = None
    source_code: str | None = None
    wasm_path: str | None = None
    status: str | None = None
    is_latest: bool | None = None


class PluginVersionResponse(PluginVersionBase):
    id: str
    plugin_id: str
    is_latest: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )