from sqlalchemy.orm import Session

from app.models.plugin_version import PluginVersion


class PluginVersionRepository:

    @staticmethod
    def create(
        db: Session,
        plugin_version: PluginVersion,
    ) -> PluginVersion:
        db.add(plugin_version)
        db.commit()
        db.refresh(plugin_version)
        return plugin_version

    @staticmethod
    def get_versions(
        db: Session,
        plugin_id: str,
    ):
        return (
            db.query(PluginVersion)
            .filter(PluginVersion.plugin_id == plugin_id)
            .order_by(PluginVersion.version.desc())
            .all()
        )

    @staticmethod
    def get_by_plugin(
        db: Session,
        plugin_id: str,
    ):
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
    ):
        return (
            db.query(PluginVersion)
            .filter(
                PluginVersion.plugin_id == plugin_id,
                PluginVersion.is_latest == True,
            )
            .first()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        version_id: str,
    ):
        return (
            db.query(PluginVersion)
            .filter(PluginVersion.id == version_id)
            .first()
        )

    @staticmethod
    def clear_latest_flag(
        db: Session,
        plugin_id: str,
    ):
        (
            db.query(PluginVersion)
            .filter(PluginVersion.plugin_id == plugin_id)
            .update(
                {"is_latest": False},
                synchronize_session=False,
            )
        )

        db.commit()

    @staticmethod
    def delete(
        db: Session,
        version: PluginVersion,
    ):
        db.delete(version)
        db.commit()