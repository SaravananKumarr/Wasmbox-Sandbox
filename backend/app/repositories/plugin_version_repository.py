from sqlalchemy.orm import Session

from app.models.plugin_version import PluginVersion


class PluginVersionRepository:

    @staticmethod
    def create(
        db: Session,
        plugin_id: str,
        version: int,
        source_code: str,
        wasm_path: str | None = None,
    ) -> PluginVersion:

        plugin_version = PluginVersion(
            plugin_id=plugin_id,
            version=version,
            source_code=source_code,
            wasm_path=wasm_path,
        )

        db.add(plugin_version)
        db.commit()
        db.refresh(plugin_version)

        return plugin_version

    @staticmethod
    def get_versions(
        db: Session,
        plugin_id: str,
    ) -> list[PluginVersion]:

        return (
            db.query(PluginVersion)
            .filter(PluginVersion.plugin_id == plugin_id)
            .order_by(PluginVersion.version.desc())
            .all()
        )

    @staticmethod
    def get_latest(
        db: Session,
        plugin_id: str,
    ) -> PluginVersion | None:

        return (
            db.query(PluginVersion)
            .filter(PluginVersion.plugin_id == plugin_id)
            .order_by(PluginVersion.version.desc())
            .first()
        )

    @staticmethod
    def get_by_version(
        db: Session,
        plugin_id: str,
        version: int,
    ) -> PluginVersion | None:

        return (
            db.query(PluginVersion)
            .filter(
                PluginVersion.plugin_id == plugin_id,
                PluginVersion.version == version,
            )
            .first()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        plugin_id: str,
        version: int,
    ) -> PluginVersion | None:

        return (
            db.query(PluginVersion)
            .filter(
                PluginVersion.plugin_id == plugin_id,
                PluginVersion.version == version,
            )
            .first()
        )