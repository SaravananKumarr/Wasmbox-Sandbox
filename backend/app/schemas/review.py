from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rating must be between 1 and 5",
    )

    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
    )

    comment: Optional[str] = None


class ReviewResponse(ReviewBase):
    id: str
    plugin_id: str
    user_id: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class AverageRatingResponse(BaseModel):
    plugin_id: str
    average_rating: float
    total_reviews: int