from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.plugin import Plugin
from app.models.review import Review
from app.models.comment import Comment
from app.models.favorite import Favorite
from app.models.plugin_version import PluginVersion
from app.models.plugin_install import PluginInstall


class AnalyticsRepository:

    # =====================================================
    # Plugin Analytics
    # =====================================================

    def get_plugin_analytics(
        self,
        db: Session,
        plugin_id: str,
    ):

        total_downloads = (
            db.query(func.count(PluginInstall.id))
            .filter(PluginInstall.plugin_id == plugin_id)
            .scalar()
            or 0
        )

        average_rating = (
            db.query(func.avg(Review.rating))
            .filter(Review.plugin_id == plugin_id)
            .scalar()
            or 0
        )

        total_reviews = (
            db.query(func.count(Review.id))
            .filter(Review.plugin_id == plugin_id)
            .scalar()
            or 0
        )

        total_comments = (
            db.query(func.count(Comment.id))
            .filter(Comment.plugin_id == plugin_id)
            .scalar()
            or 0
        )

        total_favorites = (
            db.query(func.count(Favorite.id))
            .filter(Favorite.plugin_id == plugin_id)
            .scalar()
            or 0
        )

        total_versions = (
            db.query(func.count(PluginVersion.id))
            .filter(PluginVersion.plugin_id == plugin_id)
            .scalar()
            or 0
        )

        return {
            "plugin_id": plugin_id,
            "total_downloads": total_downloads,
            "average_rating": round(float(average_rating), 2),
            "total_reviews": total_reviews,
            "total_comments": total_comments,
            "total_favorites": total_favorites,
            "total_versions": total_versions,
        }

    # =====================================================
    # Top Rated Plugins
    # =====================================================

    def top_rated_plugins(
        self,
        db: Session,
        limit: int = 10,
    ):

        results = (
            db.query(
                Plugin.id,
                Plugin.name,
                func.avg(Review.rating).label("rating"),
            )
            .join(
                Review,
                Plugin.id == Review.plugin_id,
            )
            .group_by(
                Plugin.id,
                Plugin.name,
            )
            .order_by(
                func.avg(Review.rating).desc(),
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "plugin_id": plugin.id,
                "plugin_name": plugin.name,
                "value": round(float(plugin.rating), 2),
            }
            for plugin in results
        ]

    # =====================================================
    # Most Downloaded Plugins
    # =====================================================

    def most_downloaded_plugins(
        self,
        db: Session,
        limit: int = 10,
    ):

        results = (
            db.query(
                Plugin.id,
                Plugin.name,
                func.count(PluginInstall.id).label("downloads"),
            )
            .join(
                PluginInstall,
                Plugin.id == PluginInstall.plugin_id,
            )
            .group_by(
                Plugin.id,
                Plugin.name,
            )
            .order_by(
                func.count(PluginInstall.id).desc(),
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "plugin_id": plugin.id,
                "plugin_name": plugin.name,
                "value": plugin.downloads,
            }
            for plugin in results
        ]

    # =====================================================
    # Download Trend
    # =====================================================

    def download_trend(
        self,
        db: Session,
        plugin_id: str,
    ):

        results = (
            db.query(
                func.date(PluginInstall.installed_at).label("date"),
                func.count(PluginInstall.id).label("downloads"),
            )
            .filter(
                PluginInstall.plugin_id == plugin_id,
            )
            .group_by(
                func.date(PluginInstall.installed_at),
            )
            .order_by(
                func.date(PluginInstall.installed_at),
            )
            .all()
        )

        return [
            {
                "date": str(item.date),
                "downloads": item.downloads,
            }
            for item in results
        ]


analytics_repository = AnalyticsRepository()