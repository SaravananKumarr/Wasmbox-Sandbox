import os

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.compiler.compiler_service import compiler_service
from app.compiler.storage import save_uploaded_wasm

from app.models.plugin import Plugin

from app.repositories.plugin_repository import plugin_repository
from app.repositories.category_repository import category_repository

from app.schemas.plugin import (
    PluginCreate,
    PluginImport,
    PluginUpdate,
    PluginSearchQuery,
    PluginListResponse,
)


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

        if getattr(plugin, "category_id", None):
            category = category_repository.get_category(
                db=db,
                category_id=plugin.category_id,
            )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found.",
                )

        source_path = compiler_service.save_plugin(
            source_code=plugin.source_code,
            language=plugin.language,
        )

        wasm_path = compiler_service.compile(source_path)

        created_plugin = plugin_repository.create_plugin(
            db=db,
            plugin=plugin,
            user_id=user_id,
            wasm_path=wasm_path,
        )

        return created_plugin

    def import_plugin(
        self,
        db: Session,
        plugin: PluginImport,
        file: UploadFile,
        user_id: str,
    ) -> Plugin:

        if getattr(plugin, "category_id", None):
            category = category_repository.get_category(
                db=db,
                category_id=plugin.category_id,
            )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found.",
                )

        wasm_path = save_uploaded_wasm(file)

        created_plugin = plugin_repository.create_imported_plugin(
            db=db,
            plugin=plugin,
            wasm_path=wasm_path,
            user_id=user_id,
        )

        return created_plugin

    def get_plugins(
        self,
        db: Session,
        user_id: str,
        query: PluginSearchQuery,
    ) -> PluginListResponse:

        total, plugins = plugin_repository.get_plugins(
            db=db,
            user_id=user_id,
            query=query,
        )

        pages = (
            (total + query.limit - 1) // query.limit
            if total
            else 1
        )

        return PluginListResponse(
            page=query.page,
            limit=query.limit,
            total=total,
            pages=pages,
            items=plugins,
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

        if getattr(plugin_data, "category_id", None):
            category = category_repository.get_category(
                db=db,
                category_id=plugin_data.category_id,
            )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found.",
                )

        wasm_path = None

        if plugin_data.source_code is not None:

            language = plugin_data.language or plugin.language

            source_path = compiler_service.save_plugin(
                source_code=plugin_data.source_code,
                language=language,
            )

            wasm_path = compiler_service.compile(source_path)

        updated_plugin = plugin_repository.update_plugin(
            db=db,
            db_plugin=plugin,
            plugin=plugin_data,
            wasm_path=wasm_path,
        )

        return updated_plugin

    def download_plugin(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
    ) -> tuple[str, str]:

        plugin = self.get_plugin(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id,
        )

        if not plugin.wasm_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compiled WASM file not found.",
            )

        if not os.path.isfile(plugin.wasm_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="WASM file does not exist.",
            )

        filename = f"{plugin.name.replace(' ', '_')}.wasm"

        return plugin.wasm_path, filename

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