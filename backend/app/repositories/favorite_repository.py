from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.favorite import Favorite


class FavoriteRepository:
    """
    Repository responsible for Favorite database operations.
    """

    # -------------------------------------
    # Add Favorite
    # -------------------------------------

    def add_favorite(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
    ) -> Favorite:

        favorite = Favorite(
            plugin_id=plugin_id,
            user_id=user_id,
        )

        db.add(favorite)
        db.commit()
        db.refresh(favorite)

        return favorite

    # -------------------------------------
    # Get Favorite
    # -------------------------------------

    def get_favorite(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
    ) -> Favorite | None:

        return (
            db.query(Favorite)
            .filter(
                Favorite.plugin_id == plugin_id,
                Favorite.user_id == user_id,
            )
            .first()
        )

    # -------------------------------------
    # My Favorites
    # -------------------------------------

    def get_user_favorites(
        self,
        db: Session,
        user_id: str,
    ):

        return (
            db.query(Favorite)
            .filter(
                Favorite.user_id == user_id
            )
            .order_by(
                Favorite.created_at.desc()
            )
            .all()
        )

    # -------------------------------------
    # Remove Favorite
    # -------------------------------------

    def remove_favorite(
        self,
        db: Session,
        favorite: Favorite,
    ):

        db.delete(favorite)
        db.commit()

    # -------------------------------------
    # Favorite Count
    # -------------------------------------

    def favorite_count(
        self,
        db: Session,
        plugin_id: str,
    ):

        count = (
            db.query(func.count(Favorite.id))
            .filter(
                Favorite.plugin_id == plugin_id
            )
            .scalar()
        )

        return {
            "plugin_id": plugin_id,
            "favorite_count": count,
        }


favorite_repository = FavoriteRepository()