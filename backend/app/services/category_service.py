from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.category_repository import category_repository
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:
    """
    Business logic for Category operations.
    """

    # -------------------------------------
    # Create Category
    # -------------------------------------

    def create_category(
        self,
        db: Session,
        category: CategoryCreate,
    ):

        existing = category_repository.get_category_by_name(
            db=db,
            name=category.name,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists.",
            )

        return category_repository.create_category(
            db=db,
            category=category,
        )

    # -------------------------------------
    # Get Category
    # -------------------------------------

    def get_category(
        self,
        db: Session,
        category_id: str,
    ):

        category = category_repository.get_category(
            db=db,
            category_id=category_id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        return category

    # -------------------------------------
    # Get Categories
    # -------------------------------------

    def get_categories(
        self,
        db: Session,
    ):

        return category_repository.get_categories(db)

    # -------------------------------------
    # Update Category
    # -------------------------------------

    def update_category(
        self,
        db: Session,
        category_id: str,
        category: CategoryUpdate,
    ):

        db_category = category_repository.get_category(
            db=db,
            category_id=category_id,
        )

        if db_category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        return category_repository.update_category(
            db=db,
            db_category=db_category,
            category=category,
        )

    # -------------------------------------
    # Delete Category
    # -------------------------------------

    def delete_category(
        self,
        db: Session,
        category_id: str,
    ):

        db_category = category_repository.get_category(
            db=db,
            category_id=category_id,
        )

        if db_category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        category_repository.delete_category(
            db=db,
            db_category=db_category,
        )

        return {
            "message": "Category deleted successfully."
        }


category_service = CategoryService()