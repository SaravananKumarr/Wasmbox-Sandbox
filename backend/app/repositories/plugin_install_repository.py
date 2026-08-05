from sqlalchemy.orm import Session

from app.models.plugin_install import PluginInstall


class PluginInstallRepository:

    @staticmethod
    def create(
        db: Session,
        install: PluginInstall,
    ) -> PluginInstall:
        db.add(install)
        db.commit()
        db.refresh(install)
        return install

    @staticmethod
    def get_by_id(
        db: Session,
        install_id: str,
    ) -> PluginInstall | None:
        return (
            db.query(PluginInstall)
            .filter(
                PluginInstall.id == install_id
            )
            .first()
        )

    @staticmethod
    def get_by_plugin_and_user(
        db: Session,
        plugin_id: str,
        user_id: str,
    ) -> PluginInstall | None:
        return (
            db.query(PluginInstall)
            .filter(
                PluginInstall.plugin_id == plugin_id,
                PluginInstall.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def get_user_installs(
        db: Session,
        user_id: str,
        page: int = 1,
        limit: int = 10,
    ):
        query = (
            db.query(PluginInstall)
            .filter(
                PluginInstall.user_id == user_id
            )
        )

        total = query.count()

        installs = (
            query.order_by(
                PluginInstall.installed_at.desc()
            )
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return total, installs

    @staticmethod
    def count_installs(
        db: Session,
        plugin_id: str,
    ) -> int:
        return (
            db.query(PluginInstall)
            .filter(
                PluginInstall.plugin_id == plugin_id
            )
            .count()
        )

    @staticmethod
    def delete(
        db: Session,
        install: PluginInstall,
    ) -> None:
        db.delete(install)
        db.commit()