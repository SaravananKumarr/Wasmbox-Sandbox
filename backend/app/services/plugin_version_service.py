from sqlalchemy.orm import Session

from app.models.plugin import Plugin
from app.models.plugin_version import PluginVersion
from app.repositories.plugin_version_repository import PluginVersionRepository


class PluginVersionService:

    @staticmethod
    def create_version(
        db: Session,
        plugin: Plugin,
    ) -> PluginVersion:
        """
        Create a new version of the plugin.
        """

        latest = PluginVersionRepository.get_latest(
            db=db,
            plugin_id=plugin.id,
        )

        if latest:
            next_version = latest.version + 1
        else:
            next_version = 1

        return PluginVersionRepository.create(
            db=db,
            plugin_id=plugin.id,
            version=next_version,
            source_code=plugin.source_code,
            wasm_path=plugin.wasm_path,
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
    def get_version(
        db: Session,
        plugin_id: str,
        version: int,
    ):
        return PluginVersionRepository.get_by_version(
            db=db,
            plugin_id=plugin_id,
            version=version,
        )

    @staticmethod
    def restore_version(
        db: Session,
        plugin: Plugin,
        version: int,
    ):
        """
        Restore the plugin to a previous version.
        A new version is created after restoration so the history remains intact.
        """

        old_version = PluginVersionRepository.get_by_version(
            db=db,
            plugin_id=plugin.id,
            version=version,
        )

        if old_version is None:
            return None

        # Restore plugin data
        plugin.source_code = old_version.source_code
        plugin.wasm_path = old_version.wasm_path

        db.commit()
        db.refresh(plugin)

        # Save the restored state as a new version
        PluginVersionService.create_version(
            db=db,
            plugin=plugin,
        )

        return plugin