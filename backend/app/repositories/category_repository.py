from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryRepository:
    """
    Repository for Category database operations.
    """

    # -------------------------------------
    # Create Category
    # -------------------------------------

    def create_category(
        self,
        db: Session,
        category: CategoryCreate,
    ) -> Category:

        db_category = Category(
            name=category.name,
            description=category.description,
        )

        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        return db_category

    # -------------------------------------
    # Get Category By ID
    # -------------------------------------

    def get_category(
        self,
        db: Session,
        category_id: str,
    ) -> Category | None:

        return (
            db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    # -------------------------------------
    # Get Category By Name
    # -------------------------------------

    def get_category_by_name(
        self,
        db: Session,
        name: str,
    ) -> Category | None:

        return (
            db.query(Category)
            .filter(Category.name == name)
            .first()
        )

    # -------------------------------------
    # Get All Categories
    # -------------------------------------

    def get_categories(
        self,
        db: Session,
    ):

        return (
            db.query(Category)
            .order_by(Category.name.asc())
            .all()
        )

    # -------------------------------------
    # Update Category
    # -------------------------------------

    def update_category(
        self,
        db: Session,
        db_category: Category,
        category: CategoryUpdate,
    ) -> Category:

        update_data = category.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)

        return db_category

    # -------------------------------------
    # Delete Category
    # -------------------------------------

    def delete_category(
        self,
        db: Session,
        db_category: Category,
    ):

        db.delete(db_category)
        db.commit()


category_repository = CategoryRepository()