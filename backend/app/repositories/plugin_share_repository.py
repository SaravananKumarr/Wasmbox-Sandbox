from sqlalchemy.orm import Session

from app.models.plugin_share import PluginShare


class PluginShareRepository:

    @staticmethod
    def create(
        db: Session,
        plugin_share: PluginShare,
    ) -> PluginShare:
        db.add(plugin_share)
        db.commit()
        db.refresh(plugin_share)
        return plugin_share

    @staticmethod
    def get_by_id(
        db: Session,
        share_id: str,
    ) -> PluginShare | None:
        return (
            db.query(PluginShare)
            .filter(PluginShare.id == share_id)
            .first()
        )

    @staticmethod
    def get_by_plugin_and_user(
        db: Session,
        plugin_id: str,
        user_id: str,
    ) -> PluginShare | None:
        return (
            db.query(PluginShare)
            .filter(
                PluginShare.plugin_id == plugin_id,
                PluginShare.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def get_plugin_shares(
        db: Session,
        plugin_id: str,
    ) -> list[PluginShare]:
        return (
            db.query(PluginShare)
            .filter(
                PluginShare.plugin_id == plugin_id
            )
            .all()
        )

    @staticmethod
    def get_user_shared_plugins(
        db: Session,
        user_id: str,
    ) -> list[PluginShare]:
        return (
            db.query(PluginShare)
            .filter(
                PluginShare.user_id == user_id
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        plugin_share: PluginShare,
    ) -> PluginShare:
        db.commit()
        db.refresh(plugin_share)
        return plugin_share

    @staticmethod
    def delete(
        db: Session,
        plugin_share: PluginShare,
    ) -> None:
        db.delete(plugin_share)
        db.commit()