from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.plugin_repository import plugin_repository
from app.repositories.favorite_repository import favorite_repository


class FavoriteService:
    """
    Business logic for Favorite operations.
    """

    # ----------------------------------------
    # Add Favorite
    # ----------------------------------------

    def add_favorite(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
    ):

        # Check plugin exists
        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        # Already favorited?
        existing = favorite_repository.get_favorite(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Plugin already added to favorites.",
            )

        return favorite_repository.add_favorite(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id,
        )

    # ----------------------------------------
    # Remove Favorite
    # ----------------------------------------

    def remove_favorite(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
    ):

        favorite = favorite_repository.get_favorite(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id,
        )

        if favorite is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found.",
            )

        favorite_repository.remove_favorite(
            db=db,
            favorite=favorite,
        )

        return {
            "message": "Plugin removed from favorites."
        }

    # ----------------------------------------
    # My Favorites
    # ----------------------------------------

    def get_my_favorites(
        self,
        db: Session,
        user_id: str,
    ):

        return favorite_repository.get_user_favorites(
            db=db,
            user_id=user_id,
        )

    # ----------------------------------------
    # Favorite Count
    # ----------------------------------------

    def get_favorite_count(
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

        return favorite_repository.favorite_count(
            db=db,
            plugin_id=plugin_id,
        )


favorite_service = FavoriteService()