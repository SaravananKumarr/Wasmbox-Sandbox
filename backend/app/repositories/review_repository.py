from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.review import Review
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
)


class ReviewRepository:

    # ----------------------------------
    # Create Review
    # ----------------------------------

    def create_review(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
        review: ReviewCreate,
    ) -> Review:

        db_review = Review(
            plugin_id=plugin_id,
            user_id=user_id,
            rating=review.rating,
            comment=review.comment,
        )

        db.add(db_review)
        db.commit()
        db.refresh(db_review)

        return db_review

    # ----------------------------------
    # Get Review by ID
    # ----------------------------------

    def get_review(
        self,
        db: Session,
        review_id: str,
    ) -> Review | None:

        return (
            db.query(Review)
            .filter(
                Review.id == review_id
            )
            .first()
        )

    # ----------------------------------
    # Get User Review
    # ----------------------------------

    def get_user_review(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
    ) -> Review | None:

        return (
            db.query(Review)
            .filter(
                Review.plugin_id == plugin_id,
                Review.user_id == user_id,
            )
            .first()
        )

    # ----------------------------------
    # Get Plugin Reviews
    # ----------------------------------

    def get_plugin_reviews(
        self,
        db: Session,
        plugin_id: str,
    ):

        return (
            db.query(Review)
            .filter(
                Review.plugin_id == plugin_id
            )
            .order_by(
                Review.created_at.desc()
            )
            .all()
        )

    # ----------------------------------
    # Update Review
    # ----------------------------------

    def update_review(
        self,
        db: Session,
        db_review: Review,
        review: ReviewUpdate,
    ) -> Review:

        update_data = review.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(
                db_review,
                key,
                value,
            )

        db.commit()
        db.refresh(db_review)

        return db_review

    # ----------------------------------
    # Delete Review
    # ----------------------------------

    def delete_review(
        self,
        db: Session,
        db_review: Review,
    ):

        db.delete(db_review)
        db.commit()

    # ----------------------------------
    # Average Rating
    # ----------------------------------

    def get_average_rating(
        self,
        db: Session,
        plugin_id: str,
    ):

        average, total = (
            db.query(
                func.avg(Review.rating),
                func.count(Review.id),
            )
            .filter(
                Review.plugin_id == plugin_id
            )
            .first()
        )

        return {
            "plugin_id": plugin_id,
            "average_rating": round(
                average or 0,
                2,
            ),
            "total_reviews": total,
        }


review_repository = ReviewRepository()