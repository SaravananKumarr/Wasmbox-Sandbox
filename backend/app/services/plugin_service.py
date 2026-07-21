from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.compiler.compiler_service import compiler_service
from app.models.plugin import Plugin
from app.repositories.plugin_repository import plugin_repository
from app.schemas.plugin import PluginCreate, PluginUpdate


class PluginService:
    """
    Business logic for Plugin operations.
    """

    def create_plugin(
        self,
        db: Session,
        plugin: PluginCreate,
        user_id: str,
    ) -> Plugin:

        # Step 1: Save source code into storage/plugins/
        source_path = compiler_service.save_plugin(
            source_code=plugin.source_code,
            language=plugin.language,
        )

        # Step 2: Generate placeholder WASM file
        wasm_path = compiler_service.compile(source_path)

        # Step 3: Save plugin into database with wasm_path
        created_plugin = plugin_repository.create_plugin(
            db=db,
            plugin=plugin,
            user_id=user_id,
            wasm_path=wasm_path,
        )

        return created_plugin

    def get_plugins(
        self,
        db: Session,
        user_id: str,
    ) -> list[Plugin]:

        return plugin_repository.get_plugins_by_user(
            db=db,
            user_id=user_id,
        )

    def get_plugin(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
    ) -> Plugin:

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found",
            )

        if plugin.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this plugin.",
            )

        return plugin

    def update_plugin(
        self,
        db: Session,
        plugin_id: str,
        plugin_data: PluginUpdate,
        user_id: str,
    ) -> Plugin:

        plugin = self.get_plugin(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id,
        )

        return plugin_repository.update_plugin(
            db=db,
            db_plugin=plugin,
            plugin=plugin_data,
        )

    def delete_plugin(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
    ) -> dict:

        plugin = self.get_plugin(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id,
        )

        plugin_repository.delete_plugin(
            db=db,
            db_plugin=plugin,
        )

        return {
            "message": "Plugin deleted successfully."
        }


plugin_service = PluginService()