from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PluginVersionResponse(BaseModel):
    id: str
    plugin_id: str
    version: int
    source_code: str
    wasm_path: str | None = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )