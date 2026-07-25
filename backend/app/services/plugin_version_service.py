import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.plugin import Plugin
from app.models.plugin_version import PluginVersion
from app.repositories.plugin_version_repository import PluginVersionRepository
from app.schemas.plugin_version import (
    PluginVersionCreate,
    PluginVersionUpdate,
)


class PluginVersionService:
    VERSION_PATTERN = r"^\d+\.\d+\.\d+$"

    @staticmethod
    def validate_version(version: str):
        if not re.match(PluginVersionService.VERSION_PATTERN, version):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Version must follow semantic versioning (e.g. 1.0.0)",
            )

    @staticmethod
    def create_version(
        db: Session,
        plugin: Plugin,
        data: PluginVersionCreate,
    ) -> PluginVersion:

        PluginVersionService.validate_version(data.version)

        existing_versions = PluginVersionRepository.get_versions(
            db=db,
            plugin_id=plugin.id,
        )

        for version in existing_versions:
            if version.version == data.version:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Version already exists",
                )

        PluginVersionRepository.clear_latest_flag(
            db=db,
            plugin_id=plugin.id,
        )

        plugin_version = PluginVersion(
            plugin_id=plugin.id,
            version=data.version,
            title=data.title,
            changelog=data.changelog,
            release_notes=data.release_notes,
            source_code=data.source_code,
            wasm_path=data.wasm_path,
            status=data.status,
            is_latest=True,
        )

        return PluginVersionRepository.create(
            db=db,
            plugin_version=plugin_version,
        )

    @staticmethod
    def get_versions(
        db: Session,
        plugin_id: str,
    ):
        return PluginVersionRepository.get_versions(
            db=db,
            plugin_id=plugin_id,
        )

    @staticmethod
    def get_latest_version(
        db: Session,
        plugin_id: str,
    ):
        version = PluginVersionRepository.get_latest(
            db=db,
            plugin_id=plugin_id,
        )

        if version is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No versions found",
            )

        return version

    @staticmethod
    def update_version(
        db: Session,
        version_id: str,
        data: PluginVersionUpdate,
    ):

        version = PluginVersionRepository.get_by_id(
            db=db,
            version_id=version_id,
        )

        if version is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Version not found",
            )

        update_data = data.model_dump(exclude_unset=True)

        if "version" in update_data:
            PluginVersionService.validate_version(update_data["version"])

        for key, value in update_data.items():
            setattr(version, key, value)

        db.commit()
        db.refresh(version)

        return version

    @staticmethod
    def delete_version(
        db: Session,
        version_id: str,
    ):

        version = PluginVersionRepository.get_by_id(
            db=db,
            version_id=version_id,
        )

        if version is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Version not found",
            )

        PluginVersionRepository.delete(
            db=db,
            version=version,
        )

        return {
            "message": "Version deleted successfully"
        }

    @staticmethod
    def restore_version(
        db: Session,
        plugin: Plugin,
        version_id: str,
    ):

        old_version = PluginVersionRepository.get_by_id(
            db=db,
            version_id=version_id,
        )

        if old_version is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Version not found",
            )

        plugin.source_code = old_version.source_code
        plugin.wasm_path = old_version.wasm_path

        db.commit()
        db.refresh(plugin)

        PluginVersionRepository.clear_latest_flag(
            db=db,
            plugin_id=plugin.id,
        )

        restored = PluginVersion(
            plugin_id=plugin.id,
            version=old_version.version,
            title=old_version.title,
            changelog=f"Restored from version {old_version.version}",
            release_notes=old_version.release_notes,
            source_code=old_version.source_code,
            wasm_path=old_version.wasm_path,
            status="stable",
            is_latest=True,
        )

        return PluginVersionRepository.create(
            db=db,
            plugin_version=restored,
        )