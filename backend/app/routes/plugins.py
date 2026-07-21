from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.models.plugin import Plugin
from app.schemas.plugin import PluginCreate, PluginUpdate, PluginOut
from app.utils.response import success, error

router = APIRouter()


@router.get("/plugins", response_model=dict)
def list_plugins(db: Session = Depends(get_db)):
    plugins = db.query(Plugin).all()
    return success("Plugins retrieved", [PluginOut.model_validate(p).model_dump() for p in plugins])


@router.get("/plugin/{plugin_id}", response_model=dict)
def get_plugin(plugin_id: str, db: Session = Depends(get_db)):
    plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return success("Plugin retrieved", PluginOut.model_validate(plugin).model_dump())


@router.post("/plugin", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_plugin(plugin_data: PluginCreate, db: Session = Depends(get_db)):
    plugin = Plugin(
        name=plugin_data.name,
        owner=plugin_data.owner,
        source_code=plugin_data.source_code,
        is_public=plugin_data.is_public,
        wasm_binary=None,
    )
    db.add(plugin)
    db.commit()
    db.refresh(plugin)
    return success("Plugin created", PluginOut.model_validate(plugin).model_dump())


@router.put("/plugin/{plugin_id}", response_model=dict)
def update_plugin(plugin_id: str, plugin_data: PluginUpdate, db: Session = Depends(get_db)):
    plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    if plugin_data.name is not None:
        plugin.name = plugin_data.name
    if plugin_data.source_code is not None:
        plugin.source_code = plugin_data.source_code
    if plugin_data.is_public is not None:
        plugin.is_public = plugin_data.is_public
    db.commit()
    db.refresh(plugin)
    return success("Plugin updated", PluginOut.model_validate(plugin).model_dump())


@router.delete("/plugin/{plugin_id}", response_model=dict)
def delete_plugin(plugin_id: str, db: Session = Depends(get_db)):
    plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    db.delete(plugin)
    db.commit()
    return success("Plugin deleted")
