from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.marketplace import MarketplacePlugin
from app.models.plugin import Plugin


class MarketplaceRepository:

    @staticmethod
    def create(
        db: Session,
        marketplace: MarketplacePlugin,
    ) -> MarketplacePlugin:
        db.add(marketplace)
        db.commit()
        db.refresh(marketplace)
        return marketplace

    @staticmethod
    def get_by_plugin_id(
        db: Session,
        plugin_id: str,
    ) -> MarketplacePlugin | None:
        return (
            db.query(MarketplacePlugin)
            .filter(
                MarketplacePlugin.plugin_id == plugin_id
            )
            .first()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        marketplace_id: str,
    ) -> MarketplacePlugin | None:
        return (
            db.query(MarketplacePlugin)
            .filter(
                MarketplacePlugin.id == marketplace_id
            )
            .first()
        )

    @staticmethod
    def get_published_plugins(
        db: Session,
        page: int = 1,
        limit: int = 10,
    ):
        query = (
            db.query(MarketplacePlugin)
            .filter(
                MarketplacePlugin.is_published.is_(True)
            )
        )

        total = query.count()

        items = (
            query.order_by(
                MarketplacePlugin.published_at.desc()
            )
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return total, items

    @staticmethod
    def get_featured_plugins(
        db: Session,
        limit: int = 10,
    ):
        return (
            db.query(MarketplacePlugin)
            .filter(
                MarketplacePlugin.is_published.is_(True),
                MarketplacePlugin.featured.is_(True),
            )
            .order_by(
                MarketplacePlugin.downloads.desc()
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_trending_plugins(
        db: Session,
        limit: int = 10,
    ):
        return (
            db.query(MarketplacePlugin)
            .filter(
                MarketplacePlugin.is_published.is_(True)
            )
            .order_by(
                MarketplacePlugin.downloads.desc(),
                MarketplacePlugin.views.desc(),
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def search_plugins(
        db: Session,
        search: str | None,
        category: str | None,
        language: str | None,
        sort_by: str,
        page: int,
        limit: int,
    ):
        query = (
            db.query(MarketplacePlugin)
            .join(Plugin)
            .filter(
                MarketplacePlugin.is_published.is_(True)
            )
        )

        if search:
            query = query.filter(
                or_(
                    Plugin.name.ilike(f"%{search}%"),
                    Plugin.description.ilike(f"%{search}%"),
                )
            )

        if category:
            query = query.filter(
                Plugin.category == category
            )

        if language:
            query = query.filter(
                Plugin.language == language
            )

        if sort_by == "downloads":
            query = query.order_by(
                MarketplacePlugin.downloads.desc()
            )

        elif sort_by == "views":
            query = query.order_by(
                MarketplacePlugin.views.desc()
            )

        elif sort_by == "name":
            query = query.order_by(
                Plugin.name.asc()
            )

        else:
            query = query.order_by(
                MarketplacePlugin.published_at.desc()
            )

        total = query.count()

        items = (
            query.offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return total, items

    @staticmethod
    def get_statistics(
        db: Session,
    ):
        total_plugins = db.query(Plugin).count()

        published_plugins = (
            db.query(MarketplacePlugin)
            .filter(
                MarketplacePlugin.is_published.is_(True)
            )
            .count()
        )

        featured_plugins = (
            db.query(MarketplacePlugin)
            .filter(
                MarketplacePlugin.is_published.is_(True),
                MarketplacePlugin.featured.is_(True),
            )
            .count()
        )

        total_downloads, total_views = (
            db.query(
                func.coalesce(
                    func.sum(MarketplacePlugin.downloads),
                    0,
                ),
                func.coalesce(
                    func.sum(MarketplacePlugin.views),
                    0,
                ),
            )
            .one()
        )

        return {
            "total_plugins": total_plugins,
            "published_plugins": published_plugins,
            "featured_plugins": featured_plugins,
            "total_downloads": total_downloads,
            "total_views": total_views,
        }

    @staticmethod
    def increment_downloads(
        db: Session,
        marketplace: MarketplacePlugin,
    ) -> MarketplacePlugin:
        marketplace.downloads += 1
        db.commit()
        db.refresh(marketplace)
        return marketplace

    @staticmethod
    def increment_views(
        db: Session,
        marketplace: MarketplacePlugin,
    ) -> MarketplacePlugin:
        marketplace.views += 1
        db.commit()
        db.refresh(marketplace)
        return marketplace

    @staticmethod
    def update(
        db: Session,
        marketplace: MarketplacePlugin,
    ) -> MarketplacePlugin:
        db.commit()
        db.refresh(marketplace)
        return marketplace

    @staticmethod
    def delete(
        db: Session,
        marketplace: MarketplacePlugin,
    ) -> None:
        db.delete(marketplace)
        db.commit()