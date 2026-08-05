from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# -----------------------------
# Base Schema
# -----------------------------
class CollectionBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    is_public: bool = False


# -----------------------------
# Create Collection
# -----------------------------
class CollectionCreate(CollectionBase):
    pass


# -----------------------------
# Update Collection
# -----------------------------
class CollectionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    is_public: bool | None = None


# -----------------------------
# Add Plugin to Collection
# -----------------------------
class CollectionPluginCreate(BaseModel):
    plugin_id: UUID


# -----------------------------
# Remove Plugin from Collection
# -----------------------------
class CollectionPluginDelete(BaseModel):
    plugin_id: UUID


# -----------------------------
# Collection Response
# -----------------------------
class CollectionResponse(CollectionBase):
    id: UUID
    user_id: UUID
    is_featured: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# -----------------------------
# Collection Plugin Response
# -----------------------------
class CollectionPluginResponse(BaseModel):
    id: UUID
    collection_id: UUID
    plugin_id: UUID
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# -----------------------------
# Collection Statistics
# -----------------------------
class CollectionStatisticsResponse(BaseModel):
    total_plugins: int
    total_public_collections: int
    total_private_collections: int


# -----------------------------
# Paginated Response
# -----------------------------
class CollectionListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[CollectionResponse]