from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.schemas.plugin import PluginCreate
from app.schemas.plugin import PluginUpdate
from app.services import plugin_service

router = APIRouter()


@router.get("/plugins")
def list_plugins(db: Session = Depends(get_db)):

    return plugin_service.list_plugins(db)


@router.get("/plugins/{plugin_id}")
def get_plugin(plugin_id: str, db: Session = Depends(get_db)):

    plugin = plugin_service.get_plugin(db, plugin_id)
    if plugin is None:
        raise HTTPException(status_code=404, detail="Plugin not found")

    return plugin


@router.post("/plugins", status_code=201)
def create_plugin(data: PluginCreate, db: Session = Depends(get_db)):

    return plugin_service.create_plugin(db, data)


@router.put("/plugins/{plugin_id}")
def update_plugin(plugin_id: str, data: PluginUpdate, db: Session = Depends(get_db)):

    plugin = plugin_service.update_plugin(db, plugin_id, data)
    if plugin is None:
        raise HTTPException(status_code=404, detail="Plugin not found")

    return plugin


@router.delete("/plugins/{plugin_id}")
def delete_plugin(plugin_id: str, db: Session = Depends(get_db)):

    deleted = plugin_service.delete_plugin(db, plugin_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Plugin not found")

    return {"success": True, "id": plugin_id}
