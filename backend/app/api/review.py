from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User

from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    AverageRatingResponse,
    RatingDistributionResponse,
)

from app.services.review_service import review_service

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


# =====================================================
# Create Review
# =====================================================

@router.post(
    "/{plugin_id}",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    plugin_id: str,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.create_review(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
        review=review,
    )


# =====================================================
# Get Plugin Reviews
# =====================================================

@router.get(
    "/{plugin_id}",
    response_model=list[ReviewResponse],
)
def get_plugin_reviews(
    plugin_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query(
        "latest",
        pattern="^(latest|oldest|highest|lowest)$",
    ),
    db: Session = Depends(get_db),
):
    return review_service.get_plugin_reviews(
        db=db,
        plugin_id=plugin_id,
        skip=skip,
        limit=limit,
        sort=sort,
    )


# =====================================================
# Get Average Rating
# =====================================================

@router.get(
    "/{plugin_id}/average",
    response_model=AverageRatingResponse,
)
def get_average_rating(
    plugin_id: str,
    db: Session = Depends(get_db),
):
    return review_service.get_average_rating(
        db=db,
        plugin_id=plugin_id,
    )


# =====================================================
# Rating Distribution
# =====================================================

@router.get(
    "/{plugin_id}/distribution",
    response_model=RatingDistributionResponse,
)
def rating_distribution(
    plugin_id: str,
    db: Session = Depends(get_db),
):
    return review_service.get_rating_distribution(
        db=db,
        plugin_id=plugin_id,
    )


# =====================================================
# Helpful Vote
# =====================================================

@router.post(
    "/{review_id}/helpful",
)
def mark_helpful(
    review_id: str,
    db: Session = Depends(get_db),
):
    return review_service.mark_helpful(
        db=db,
        review_id=review_id,
    )


# =====================================================
# Update Review
# =====================================================

@router.put(
    "/{review_id}",
    response_model=ReviewResponse,
)
def update_review(
    review_id: str,
    review: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.update_review(
        db=db,
        review_id=review_id,
        user_id=current_user.id,
        review=review,
    )


# =====================================================
# Delete Review
# =====================================================

@router.delete(
    "/{review_id}",
)
def delete_review(
    review_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.delete_review(
        db=db,
        review_id=review_id,
        user_id=current_user.id,
    )