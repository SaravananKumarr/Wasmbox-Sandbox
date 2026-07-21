from sqlalchemy.orm import Session

from app.models.plugin import Plugin
from app.schemas.plugin import PluginCreate, PluginUpdate


class PluginRepository:
    """
    Repository responsible for all Plugin database operations.
    """

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
            user_id=user_id,
        )

        db.add(db_plugin)
        db.commit()
        db.refresh(db_plugin)

        return db_plugin

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

    def get_plugins_by_user(
        self,
        db: Session,
        user_id: str,
    ) -> list[Plugin]:

        return (
            db.query(Plugin)
            .filter(Plugin.user_id == user_id)
            .order_by(Plugin.created_at.desc())
            .all()
        )

    def update_plugin(
        self,
        db: Session,
        db_plugin: Plugin,
        plugin: PluginUpdate,
    ) -> Plugin:

        update_data = plugin.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_plugin, key, value)

        db.commit()
        db.refresh(db_plugin)

        return db_plugin

    def delete_plugin(
        self,
        db: Session,
        db_plugin: Plugin,
    ) -> None:

        db.delete(db_plugin)
        db.commit()


plugin_repository = PluginRepository()