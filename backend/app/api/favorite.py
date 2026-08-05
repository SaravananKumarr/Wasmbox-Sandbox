from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User

from app.schemas.favorite import (
    FavoriteResponse,
    FavoriteCountResponse,
)

from app.services.favorite_service import favorite_service

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"],
)


# ==========================================
# Add Favorite
# ==========================================

@router.post(
    "/{plugin_id}",
    response_model=FavoriteResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_favorite(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return favorite_service.add_favorite(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )


# ==========================================
# My Favorites
# ==========================================

@router.get(
    "",
    response_model=list[FavoriteResponse],
)
def get_my_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return favorite_service.get_my_favorites(
        db=db,
        user_id=current_user.id,
    )


# ==========================================
# Remove Favorite
# ==========================================

@router.delete(
    "/{plugin_id}",
)
def remove_favorite(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return favorite_service.remove_favorite(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )


# ==========================================
# Favorite Count
# ==========================================

@router.get(
    "/{plugin_id}/count",
    response_model=FavoriteCountResponse,
)
def favorite_count(
    plugin_id: str,
    db: Session = Depends(get_db),
):
    return favorite_service.get_favorite_count(
        db=db,
        plugin_id=plugin_id,
    )