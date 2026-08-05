from sqlalchemy.orm import Session

from app.models.collection import Collection
from app.models.plugin import Plugin


class CollectionRepository:

    @staticmethod
    def create(db: Session, collection: Collection) -> Collection:
        db.add(collection)
        db.commit()
        db.refresh(collection)
        return collection

    @staticmethod
    def get_by_id(db: Session, collection_id: str) -> Collection | None:
        return (
            db.query(Collection)
            .filter(Collection.id == collection_id)
            .first()
        )

    @staticmethod
    def get_user_collections(
        db: Session,
        user_id: str,
    ) -> list[Collection]:
        return (
            db.query(Collection)
            .filter(Collection.user_id == user_id)
            .order_by(Collection.created_at.desc())
            .all()
        )

    @staticmethod
    def update(db: Session, collection: Collection) -> Collection:
        db.commit()
        db.refresh(collection)
        return collection

    @staticmethod
    def delete(db: Session, collection: Collection):
        db.delete(collection)
        db.commit()

    # -------------------------------------------------
    # Plugin Operations
    # -------------------------------------------------

    @staticmethod
    def add_plugin(
        db: Session,
        collection: Collection,
        plugin: Plugin,
    ):
        if plugin not in collection.plugins:
            collection.plugins.append(plugin)
            db.commit()
            db.refresh(collection)

    @staticmethod
    def remove_plugin(
        db: Session,
        collection: Collection,
        plugin: Plugin,
    ):
        if plugin in collection.plugins:
            collection.plugins.remove(plugin)
            db.commit()
            db.refresh(collection)

    @staticmethod
    def get_plugins(
        db: Session,
        collection: Collection,
    ) -> list[Plugin]:
        db.refresh(collection)
        return collection.plugins