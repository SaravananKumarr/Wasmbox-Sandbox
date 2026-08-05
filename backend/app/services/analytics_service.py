from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.analytics_repository import analytics_repository
from app.repositories.plugin_repository import plugin_repository


class AnalyticsService:

    # =====================================================
    # Plugin Dashboard
    # =====================================================

    def get_plugin_analytics(
        self,
        db: Session,
        plugin_id: str,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        return analytics_repository.get_plugin_analytics(
            db=db,
            plugin_id=plugin_id,
        )

    # =====================================================
    # Download Trend
    # =====================================================

    def get_download_trend(
        self,
        db: Session,
        plugin_id: str,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        return {
            "plugin_id": plugin_id,
            "trend": analytics_repository.download_trend(
                db=db,
                plugin_id=plugin_id,
            ),
        }

    # =====================================================
    # Top Rated Plugins
    # =====================================================

    def get_top_rated_plugins(
        self,
        db: Session,
        limit: int = 10,
    ):

        return analytics_repository.top_rated_plugins(
            db=db,
            limit=limit,
        )

    # =====================================================
    # Most Downloaded Plugins
    # =====================================================

    def get_most_downloaded_plugins(
        self,
        db: Session,
        limit: int = 10,
    ):

        return analytics_repository.most_downloaded_plugins(
            db=db,
            limit=limit,
        )


analytics_service = AnalyticsService()