from sqlalchemy.orm import Session

from app.models.collection import Collection
from app.repositories.collection_repository import CollectionRepository
from app.repositories.plugin_repository import PluginRepository
from app.schemas.collection import (
    CollectionCreate,
    CollectionUpdate,
)
from app.schemas.collection_plugin import CollectionPluginCreate


class CollectionService:

    @staticmethod
    def create_collection(
        db: Session,
        data: CollectionCreate,
        user_id: str,
    ) -> Collection:

        collection = Collection(
            name=data.name,
            description=data.description,
            is_public=data.is_public,
            user_id=user_id,
        )

        return CollectionRepository.create(db, collection)

    @staticmethod
    def get_collection(
        db: Session,
        collection_id: str,
    ) -> Collection:

        collection = CollectionRepository.get_by_id(
            db,
            collection_id,
        )

        if not collection:
            raise ValueError("Collection not found.")

        return collection

    @staticmethod
    def get_my_collections(
        db: Session,
        user_id: str,
    ):

        return CollectionRepository.get_user_collections(
            db,
            user_id,
        )

    @staticmethod
    def update_collection(
        db: Session,
        collection_id: str,
        data: CollectionUpdate,
        user_id: str,
    ) -> Collection:

        collection = CollectionRepository.get_by_id(
            db,
            collection_id,
        )

        if not collection:
            raise ValueError("Collection not found.")

        if collection.user_id != user_id:
            raise PermissionError(
                "You are not allowed to update this collection."
            )

        if data.name is not None:
            collection.name = data.name

        if data.description is not None:
            collection.description = data.description

        if data.is_public is not None:
            collection.is_public = data.is_public

        return CollectionRepository.update(
            db,
            collection,
        )

    @staticmethod
    def delete_collection(
        db: Session,
        collection_id: str,
        user_id: str,
    ):

        collection = CollectionRepository.get_by_id(
            db,
            collection_id,
        )

        if not collection:
            raise ValueError("Collection not found.")

        if collection.user_id != user_id:
            raise PermissionError(
                "You are not allowed to delete this collection."
            )

        CollectionRepository.delete(
            db,
            collection,
        )

    # -----------------------------------------
    # Plugin Operations
    # -----------------------------------------

    @staticmethod
    def add_plugin(
        db: Session,
        collection_id: str,
        data: CollectionPluginCreate,
        user_id: str,
    ):

        collection = CollectionRepository.get_by_id(
            db,
            collection_id,
        )

        if not collection:
            raise ValueError("Collection not found.")

        if collection.user_id != user_id:
            raise PermissionError(
                "You cannot modify this collection."
            )

        plugin = PluginRepository.get_by_id(
            db,
            data.plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        CollectionRepository.add_plugin(
            db,
            collection,
            plugin,
        )

        return collection

    @staticmethod
    def remove_plugin(
        db: Session,
        collection_id: str,
        plugin_id: str,
        user_id: str,
    ):

        collection = CollectionRepository.get_by_id(
            db,
            collection_id,
        )

        if not collection:
            raise ValueError("Collection not found.")

        if collection.user_id != user_id:
            raise PermissionError(
                "You cannot modify this collection."
            )

        plugin = PluginRepository.get_by_id(
            db,
            plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        CollectionRepository.remove_plugin(
            db,
            collection,
            plugin,
        )

        return collection

    @staticmethod
    def get_collection_plugins(
        db: Session,
        collection_id: str,
    ):

        collection = CollectionRepository.get_by_id(
            db,
            collection_id,
        )

        if not collection:
            raise ValueError("Collection not found.")

        return CollectionRepository.get_plugins(
            db,
            collection,
        )