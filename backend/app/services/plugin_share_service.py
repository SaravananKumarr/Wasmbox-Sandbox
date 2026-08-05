from sqlalchemy.orm import Session

from app.models.plugin_share import PluginShare
from app.repositories.plugin_repository import PluginRepository
from app.repositories.plugin_share_repository import PluginShareRepository
from app.repositories.user_repository import UserRepository
from app.schemas.plugin_share import (
    PluginShareCreate,
    PluginShareUpdate,
)


class PluginShareService:

    @staticmethod
    def share_plugin(
        db: Session,
        plugin_id: str,
        data: PluginShareCreate,
        current_user_id: str,
    ) -> PluginShare:

        plugin = PluginRepository.get_by_id(db, plugin_id)

        if not plugin:
            raise ValueError("Plugin not found.")

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "Only the plugin owner can share this plugin."
            )

        if data.user_id == current_user_id:
            raise ValueError(
                "You cannot share a plugin with yourself."
            )

        user = UserRepository.get_by_id(
            db,
            data.user_id,
        )

        if not user:
            raise ValueError("User not found.")

        existing_share = PluginShareRepository.get_by_plugin_and_user(
            db,
            plugin_id,
            data.user_id,
        )

        if existing_share:
            raise ValueError(
                "Plugin is already shared with this user."
            )

        plugin_share = PluginShare(
            plugin_id=plugin_id,
            user_id=data.user_id,
            permission=data.permission,
        )

        return PluginShareRepository.create(
            db,
            plugin_share,
        )

    @staticmethod
    def update_permission(
        db: Session,
        share_id: str,
        data: PluginShareUpdate,
        current_user_id: str,
    ) -> PluginShare:

        share = PluginShareRepository.get_by_id(
            db,
            share_id,
        )

        if not share:
            raise ValueError("Share not found.")

        plugin = PluginRepository.get_by_id(
            db,
            share.plugin_id,
        )

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "Only the owner can change permissions."
            )

        share.permission = data.permission

        return PluginShareRepository.update(
            db,
            share,
        )

    @staticmethod
    def remove_share(
        db: Session,
        share_id: str,
        current_user_id: str,
    ):

        share = PluginShareRepository.get_by_id(
            db,
            share_id,
        )

        if not share:
            raise ValueError("Share not found.")

        plugin = PluginRepository.get_by_id(
            db,
            share.plugin_id,
        )

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "Only the owner can remove sharing."
            )

        PluginShareRepository.delete(
            db,
            share,
        )

    @staticmethod
    def get_plugin_shares(
        db: Session,
        plugin_id: str,
        current_user_id: str,
    ):

        plugin = PluginRepository.get_by_id(
            db,
            plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "Only the owner can view shared users."
            )

        return PluginShareRepository.get_plugin_shares(
            db,
            plugin_id,
        )

    @staticmethod
    def get_shared_with_me(
        db: Session,
        current_user_id: str,
    ):

        return PluginShareRepository.get_user_shared_plugins(
            db,
            current_user_id,
        )