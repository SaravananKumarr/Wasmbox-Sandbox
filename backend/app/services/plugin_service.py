from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.plugin_repository import plugin_repository
from app.schemas.plugin import PluginCreate, PluginUpdate


class PluginService:

    def create_plugin(
        self,
        db: Session,
        plugin: PluginCreate,
        user_id: str
    ):
        return plugin_repository.create_plugin(
            db=db,
            plugin=plugin,
            user_id=user_id
        )

    def get_plugins(
        self,
        db: Session,
        user_id: str
    ):
        return plugin_repository.get_plugins_by_user(
            db=db,
            user_id=user_id
        )

    def get_plugin(
        self,
        db: Session,
        plugin_id: int,
        user_id: str
    ):
        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id
        )

        if not plugin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found"
            )

        if plugin.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        return plugin

    def update_plugin(
        self,
        db: Session,
        plugin_id: int,
        plugin_data: PluginUpdate,
        user_id: str
    ):
        plugin = self.get_plugin(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id
        )

        return plugin_repository.update_plugin(
            db=db,
            db_plugin=plugin,
            plugin=plugin_data
        )

    def delete_plugin(
        self,
        db: Session,
        plugin_id: int,
        user_id: str
    ):
        plugin = self.get_plugin(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id
        )

        plugin_repository.delete_plugin(
            db=db,
            db_plugin=plugin
        )

        return {
            "message": "Plugin deleted successfully"
        }


plugin_service = PluginService()