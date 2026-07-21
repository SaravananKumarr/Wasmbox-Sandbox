from sqlalchemy.orm import Session
from app.models.plugin import Plugin, ExecutionLog
from app.schemas.plugin import PluginCreate, PluginUpdate
import uuid


class PluginService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: PluginCreate) -> Plugin:
        plugin = Plugin(
            id=str(uuid.uuid4()),
            name=data.name,
            owner=data.owner,
            source_code=data.source_code,
            is_public=data.is_public,
        )
        self.db.add(plugin)
        self.db.commit()
        self.db.refresh(plugin)
        return plugin

    def get_all(self) -> list:
        return self.db.query(Plugin).all()

    def get_by_id(self, plugin_id: str) -> Plugin:
        return self.db.query(Plugin).filter(Plugin.id == plugin_id).first()

    def update(self, plugin_id: str, data: PluginUpdate) -> Plugin:
        plugin = self.get_by_id(plugin_id)
        if not plugin:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(plugin, field, value)
        self.db.commit()
        self.db.refresh(plugin)
        return plugin

    def delete(self, plugin_id: str) -> bool:
        plugin = self.get_by_id(plugin_id)
        if not plugin:
            return False
        self.db.delete(plugin)
        self.db.commit()
        return True
