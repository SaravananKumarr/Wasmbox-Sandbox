from sqlalchemy.orm import Session

from app.models.plugin_install import PluginInstall
from app.repositories.marketplace_repository import MarketplaceRepository
from app.repositories.plugin_install_repository import (
    PluginInstallRepository,
)
from app.repositories.plugin_repository import PluginRepository
from app.schemas.plugin_install import (
    PluginInstallListResponse,
)


class PluginInstallService:

    @staticmethod
    def install_plugin(
        db: Session,
        plugin_id: str,
        current_user_id: str,
    ) -> PluginInstall:

        plugin = PluginRepository.get_by_id(
            db,
            plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        marketplace = MarketplaceRepository.get_by_plugin_id(
            db,
            plugin_id,
        )

        if not marketplace or not marketplace.is_published:
            raise ValueError(
                "Plugin is not available in the marketplace."
            )

        existing = (
            PluginInstallRepository.get_by_plugin_and_user(
                db,
                plugin_id,
                current_user_id,
            )
        )

        if existing:
            raise ValueError(
                "Plugin already installed."
            )

        install = PluginInstall(
            plugin_id=plugin_id,
            user_id=current_user_id,
        )

        install = PluginInstallRepository.create(
            db,
            install,
        )

        MarketplaceRepository.increment_downloads(
            db,
            marketplace,
        )

        return install

    @staticmethod
    def uninstall_plugin(
        db: Session,
        plugin_id: str,
        current_user_id: str,
    ):

        install = (
            PluginInstallRepository.get_by_plugin_and_user(
                db,
                plugin_id,
                current_user_id,
            )
        )

        if not install:
            raise ValueError(
                "Plugin is not installed."
            )

        PluginInstallRepository.delete(
            db,
            install,
        )

    @staticmethod
    def get_my_plugins(
        db: Session,
        current_user_id: str,
        page: int,
        limit: int,
    ) -> PluginInstallListResponse:

        total, installs = (
            PluginInstallRepository.get_user_installs(
                db,
                current_user_id,
                page,
                limit,
            )
        )

        return PluginInstallListResponse(
            total=total,
            page=page,
            limit=limit,
            items=installs,
        )

    @staticmethod
    def installation_count(
        db: Session,
        plugin_id: str,
    ) -> int:

        return PluginInstallRepository.count_installs(
            db,
            plugin_id,
        )