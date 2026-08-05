from sqlalchemy.orm import Session

from app.models.marketplace import MarketplacePlugin
from app.repositories.marketplace_repository import MarketplaceRepository
from app.repositories.plugin_repository import PluginRepository
from app.schemas.marketplace import (
    MarketplaceListResponse,
    MarketplaceUpdate,
)
from app.schemas.marketplace_search import MarketplaceSearchFilter
from app.schemas.marketplace_stats import MarketplaceStatsResponse


class MarketplaceService:

    @staticmethod
    def publish_plugin(
        db: Session,
        plugin_id: str,
        current_user_id: str,
    ) -> MarketplacePlugin:

        plugin = PluginRepository.get_by_id(
            db,
            plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "You are not allowed to publish this plugin."
            )

        marketplace = MarketplaceRepository.get_by_plugin_id(
            db,
            plugin_id,
        )

        if marketplace:
            if marketplace.is_published:
                raise ValueError("Plugin is already published.")

            marketplace.is_published = True

            return MarketplaceRepository.update(
                db,
                marketplace,
            )

        marketplace = MarketplacePlugin(
            plugin_id=plugin_id,
            is_published=True,
        )

        return MarketplaceRepository.create(
            db,
            marketplace,
        )

    @staticmethod
    def unpublish_plugin(
        db: Session,
        plugin_id: str,
        current_user_id: str,
    ):

        plugin = PluginRepository.get_by_id(
            db,
            plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "You are not allowed to unpublish this plugin."
            )

        marketplace = MarketplaceRepository.get_by_plugin_id(
            db,
            plugin_id,
        )

        if not marketplace:
            raise ValueError("Plugin is not published.")

        marketplace.is_published = False

        return MarketplaceRepository.update(
            db,
            marketplace,
        )

    @staticmethod
    def get_marketplace(
        db: Session,
        page: int,
        limit: int,
    ) -> MarketplaceListResponse:

        total, items = MarketplaceRepository.get_published_plugins(
            db,
            page,
            limit,
        )

        return MarketplaceListResponse(
            total=total,
            page=page,
            limit=limit,
            items=items,
        )

    @staticmethod
    def search_plugins(
        db: Session,
        filters: MarketplaceSearchFilter,
    ) -> MarketplaceListResponse:

        total, items = MarketplaceRepository.search_plugins(
            db=db,
            search=filters.search,
            category=filters.category,
            language=filters.language,
            sort_by=filters.sort_by,
            page=filters.page,
            limit=filters.limit,
        )

        return MarketplaceListResponse(
            total=total,
            page=filters.page,
            limit=filters.limit,
            items=items,
        )

    @staticmethod
    def get_statistics(
        db: Session,
    ) -> MarketplaceStatsResponse:

        stats = MarketplaceRepository.get_statistics(
            db,
        )

        return MarketplaceStatsResponse(
            total_plugins=stats["total_plugins"],
            published_plugins=stats["published_plugins"],
            featured_plugins=stats["featured_plugins"],
            total_downloads=stats["total_downloads"],
            total_views=stats["total_views"],
        )

    @staticmethod
    def get_featured_plugins(
        db: Session,
        limit: int = 10,
    ):
        return MarketplaceRepository.get_featured_plugins(
            db,
            limit,
        )

    @staticmethod
    def get_trending_plugins(
        db: Session,
        limit: int = 10,
    ):
        return MarketplaceRepository.get_trending_plugins(
            db,
            limit,
        )

    @staticmethod
    def increment_download(
        db: Session,
        plugin_id: str,
    ):

        marketplace = MarketplaceRepository.get_by_plugin_id(
            db,
            plugin_id,
        )

        if not marketplace:
            raise ValueError("Marketplace entry not found.")

        return MarketplaceRepository.increment_downloads(
            db,
            marketplace,
        )

    @staticmethod
    def increment_view(
        db: Session,
        plugin_id: str,
    ):

        marketplace = MarketplaceRepository.get_by_plugin_id(
            db,
            plugin_id,
        )

        if not marketplace:
            raise ValueError("Marketplace entry not found.")

        return MarketplaceRepository.increment_views(
            db,
            marketplace,
        )

    @staticmethod
    def update_marketplace(
        db: Session,
        plugin_id: str,
        data: MarketplaceUpdate,
        current_user_id: str,
    ):

        plugin = PluginRepository.get_by_id(
            db,
            plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "You are not allowed to update this plugin."
            )

        marketplace = MarketplaceRepository.get_by_plugin_id(
            db,
            plugin_id,
        )

        if not marketplace:
            raise ValueError("Marketplace entry not found.")

        if data.featured is not None:
            marketplace.featured = data.featured

        if data.is_published is not None:
            marketplace.is_published = data.is_published

        return MarketplaceRepository.update(
            db,
            marketplace,
        )