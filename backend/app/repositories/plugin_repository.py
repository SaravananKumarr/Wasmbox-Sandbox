from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.plugin import Plugin
from app.models.category import Category
from app.models.tag import Tag

from app.schemas.plugin import (
    PluginCreate,
    PluginUpdate,
    PluginSearchQuery,
    PluginImport,
)


class PluginRepository:
    """
    Repository responsible for all Plugin database operations.
    """

    # -------------------------------------
    # Create Plugin
    # -------------------------------------

    def create_plugin(
        self,
        db: Session,
        plugin: PluginCreate,
        user_id: str,
        wasm_path: str,
    ) -> Plugin:

        db_plugin = Plugin(
            name=plugin.name,
            description=plugin.description,
            language=plugin.language,
            source_code=plugin.source_code,
            wasm_path=wasm_path,
            status="compiled",
            user_id=user_id,
            category_id=getattr(plugin, "category_id", None),
        )

        db.add(db_plugin)
        db.commit()
        db.refresh(db_plugin)

        return db_plugin

    # -------------------------------------
    # Import Existing WASM
    # -------------------------------------

    def create_imported_plugin(
        self,
        db: Session,
        plugin: PluginImport,
        wasm_path: str,
        user_id: str,
    ) -> Plugin:

        db_plugin = Plugin(
            name=plugin.name,
            description=plugin.description,
            language="wasm",
            source_code="// Imported WASM Plugin",
            wasm_path=wasm_path,
            status="compiled",
            user_id=user_id,
            category_id=getattr(plugin, "category_id", None),
        )

        db.add(db_plugin)
        db.commit()
        db.refresh(db_plugin)

        return db_plugin

    # -------------------------------------
    # Get Plugin By ID
    # -------------------------------------

    def get_plugin_by_id(
        self,
        db: Session,
        plugin_id: str,
    ) -> Plugin | None:

        return (
            db.query(Plugin)
            .filter(Plugin.id == plugin_id)
            .first()
        )

    # -------------------------------------
    # Get Plugins
    # -------------------------------------

    def get_plugins(
        self,
        db: Session,
        user_id: str,
        query: PluginSearchQuery,
    ):

        q = (
            db.query(Plugin)
            .filter(
                Plugin.user_id == user_id
            )
        )

        # -----------------------------
        # Search
        # -----------------------------

        if query.search:
            q = q.filter(
                Plugin.name.ilike(
                    f"%{query.search}%"
                )
            )

        # -----------------------------
        # Language
        # -----------------------------

        if query.language:
            q = q.filter(
                Plugin.language == query.language
            )

        # -----------------------------
        # Status
        # -----------------------------

        if query.status:
            q = q.filter(
                Plugin.status == query.status
            )

        # -----------------------------
        # Category Filter
        # -----------------------------

        if getattr(query, "category", None):
            q = (
                q.join(Category)
                .filter(
                    Category.name.ilike(query.category)
                )
            )

        # -----------------------------
        # Tag Filter
        # -----------------------------

        if getattr(query, "tag", None):
            q = (
                q.join(Plugin.tags)
                .filter(
                    Tag.name.ilike(query.tag)
                )
            )

        # Remove duplicates after joins
        q = q.distinct()

        total = q.count()

        # -----------------------------
        # Sorting
        # -----------------------------

        sort_column = getattr(
            Plugin,
            query.sort,
            Plugin.created_at,
        )

        if query.order.lower() == "asc":
            q = q.order_by(
                asc(sort_column)
            )
        else:
            q = q.order_by(
                desc(sort_column)
            )

        plugins = (
            q.offset(query.offset)
            .limit(query.limit)
            .all()
        )

        return total, plugins

    # -------------------------------------
    # Update Plugin
    # -------------------------------------

    def update_plugin(
        self,
        db: Session,
        db_plugin: Plugin,
        plugin: PluginUpdate,
        wasm_path: str | None = None,
    ) -> Plugin:

        update_data = plugin.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(db_plugin, key, value)

        if wasm_path is not None:
            db_plugin.wasm_path = wasm_path

        db.commit()
        db.refresh(db_plugin)

        return db_plugin

    # -------------------------------------
    # Delete Plugin
    # -------------------------------------

    def delete_plugin(
        self,
        db: Session,
        db_plugin: Plugin,
    ):

        db.delete(db_plugin)
        db.commit()


plugin_repository = PluginRepository()