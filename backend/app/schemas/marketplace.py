from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MarketplacePublish(BaseModel):
    is_published: bool = True


class MarketplaceUpdate(BaseModel):
    featured: bool | None = None
    is_published: bool | None = None


class MarketplaceResponse(BaseModel):
    id: str
    plugin_id: str

    is_published: bool
    featured: bool

    downloads: int
    views: int

    published_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class MarketplaceListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[MarketplaceResponse]