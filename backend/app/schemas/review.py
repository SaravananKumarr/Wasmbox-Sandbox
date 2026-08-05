from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Base
# ==========================================

class ReviewBase(BaseModel):
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rating must be between 1 and 5",
    )

    title: str = Field(
        ...,
        max_length=200,
        description="Review title",
    )

    comment: Optional[str] = None


# ==========================================
# Create
# ==========================================

class ReviewCreate(ReviewBase):
    pass


# ==========================================
# Update
# ==========================================

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
    )

    title: Optional[str] = Field(
        default=None,
        max_length=200,
    )

    comment: Optional[str] = None


# ==========================================
# Response
# ==========================================

class ReviewResponse(ReviewBase):
    id: str
    plugin_id: str
    user_id: str
    helpful_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================
# Average Rating
# ==========================================

class AverageRatingResponse(BaseModel):
    plugin_id: str
    average_rating: float
    total_reviews: int


# ==========================================
# Rating Distribution
# ==========================================

class RatingDistributionResponse(BaseModel):
    plugin_id: str
    distribution: dict[int, int]