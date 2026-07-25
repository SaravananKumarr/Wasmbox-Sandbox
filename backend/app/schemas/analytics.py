from pydantic import BaseModel, ConfigDict


# ==========================================
# Plugin Analytics
# ==========================================

class PluginAnalyticsResponse(BaseModel):
    plugin_id: str
    total_downloads: int
    average_rating: float
    total_reviews: int
    total_comments: int
    total_favorites: int
    total_versions: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================
# Download Trend
# ==========================================

class DownloadTrendItem(BaseModel):
    date: str
    downloads: int


class DownloadTrendResponse(BaseModel):
    plugin_id: str
    trend: list[DownloadTrendItem]


# ==========================================
# Top Plugins
# ==========================================

class TopPluginResponse(BaseModel):
    plugin_id: str
    plugin_name: str
    value: float