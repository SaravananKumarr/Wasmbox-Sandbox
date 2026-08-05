from pydantic import BaseModel


class MarketplaceStatsResponse(BaseModel):
    total_plugins: int
    published_plugins: int
    featured_plugins: int
    total_downloads: int
    total_views: int