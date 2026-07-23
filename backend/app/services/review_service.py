from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.plugin_repository import plugin_repository
from app.repositories.review_repository import review_repository
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
)


class ReviewService:
    """
    Business logic for Review operations.
    """

    # ------------------------------------
    # Create Review
    # ------------------------------------

    def create_review(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
        review: ReviewCreate,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        existing_review = review_repository.get_user_review(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id,
        )

        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reviewed this plugin.",
            )

        return review_repository.create_review(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id,
            review=review,
        )

    # ------------------------------------
    # Get Plugin Reviews
    # ------------------------------------

    def get_plugin_reviews(
        self,
        db: Session,
        plugin_id: str,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        return review_repository.get_plugin_reviews(
            db=db,
            plugin_id=plugin_id,
        )

    # ------------------------------------
    # Average Rating
    # ------------------------------------

    def get_average_rating(
        self,
        db: Session,
        plugin_id: str,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        return review_repository.get_average_rating(
            db=db,
            plugin_id=plugin_id,
        )

    # ------------------------------------
    # Update Review
    # ------------------------------------

    def update_review(
        self,
        db: Session,
        review_id: str,
        user_id: str,
        review: ReviewUpdate,
    ):

        db_review = review_repository.get_review(
            db=db,
            review_id=review_id,
        )

        if db_review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found.",
            )

        if db_review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can update only your own review.",
            )

        return review_repository.update_review(
            db=db,
            db_review=db_review,
            review=review,
        )

    # ------------------------------------
    # Delete Review
    # ------------------------------------

    def delete_review(
        self,
        db: Session,
        review_id: str,
        user_id: str,
    ):

        db_review = review_repository.get_review(
            db=db,
            review_id=review_id,
        )

        if db_review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found.",
            )

        if db_review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can delete only your own review.",
            )

        review_repository.delete_review(
            db=db,
            db_review=db_review,
        )

        return {
            "message": "Review deleted successfully."
        }


review_service = ReviewService()