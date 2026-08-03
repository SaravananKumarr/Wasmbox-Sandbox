from typing import Optional

from sqlalchemy.orm import Session

from app.models.plugin import Plugin
from app.schemas.plugin import PluginCreate
from app.schemas.plugin import PluginUpdate
from app.utils.time import humanize_relative


def _serialize(plugin: Plugin) -> dict:
    return {
        "id": plugin.id,
        "name": plugin.name,
        "description": plugin.description,
        "status": plugin.status,
        "executions": plugin.executions,
        "runtime": f"{round(plugin.avg_runtime_ms, 1)} ms" if plugin.avg_runtime_ms else "--",
        "updated": humanize_relative(plugin.updated_at),
        "language": plugin.language,
        "code": plugin.code,
    }


def list_plugins(db: Session) -> list[dict]:
    plugins = db.query(Plugin).order_by(Plugin.updated_at.desc()).all()
    return [_serialize(p) for p in plugins]


def get_plugin(db: Session, plugin_id: str) -> Optional[dict]:
    plugin = db.get(Plugin, plugin_id)
    return _serialize(plugin) if plugin else None


def get_plugin_model(db: Session, plugin_id: str) -> Optional[Plugin]:
    return db.get(Plugin, plugin_id)


def create_plugin(db: Session, data: PluginCreate) -> dict:
    plugin = Plugin(
        name=data.name,
        description=data.description,
        code=data.code,
        language=data.language,
    )
    db.add(plugin)
    db.commit()
    db.refresh(plugin)
    return _serialize(plugin)


def update_plugin(db: Session, plugin_id: str, data: PluginUpdate) -> Optional[dict]:
    plugin = db.get(Plugin, plugin_id)
    if plugin is None:
        return None

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(plugin, field, value)

    db.commit()
    db.refresh(plugin)
    return _serialize(plugin)


def delete_plugin(db: Session, plugin_id: str) -> bool:
    plugin = db.get(Plugin, plugin_id)
    if plugin is None:
        return False

    db.delete(plugin)
    db.commit()
    return True
