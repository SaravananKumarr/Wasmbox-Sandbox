from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PluginInstallCreate(BaseModel):
    plugin_id: str


class PluginInstallResponse(BaseModel):
    id: str
    plugin_id: str
    user_id: str
    installed_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class PluginInstallListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[PluginInstallResponse]