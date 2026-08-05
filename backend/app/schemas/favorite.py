from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FavoriteResponse(BaseModel):
    id: str
    plugin_id: str
    user_id: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class FavoriteCountResponse(BaseModel):
    plugin_id: str
    favorite_count: int