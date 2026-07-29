import os
import uuid

import wasmtime
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core import messages
from app.core.config import settings
from app.database.dependency import get_db
from app.models.plugin import Plugin
from app.models.user import User
from app.schemas.plugin import ExecuteRequest, ExecuteResponse, PluginOut, PluginUpdate
from app.services.wasm_runner import execute_plugin
from app.utils.response import success

router = APIRouter(prefix="/plugins", tags=["Plugins"])

_validation_engine = wasmtime.Engine()


def _owner_storage_dir(owner_id: str) -> str:

    path = os.path.join(settings.PLUGIN_STORAGE_DIR, owner_id)
    os.makedirs(path, exist_ok=True)

    return path


def _get_owned_plugin(plugin_id: str, current_user: User, db: Session) -> Plugin:

    plugin = db.query(Plugin).filter(Plugin.id == plugin_id).first()

    if plugin is None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plugin not found")

    if plugin.owner_id != current_user.id:

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this plugin")

    return plugin


async def _read_and_validate_wasm(file: UploadFile) -> bytes:

    if not file.filename.endswith(".wasm"):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .wasm files are accepted"
        )

    content = await file.read()

    max_bytes = settings.MAX_PLUGIN_SIZE_MB * 1024 * 1024

    if len(content) > max_bytes:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plugin file exceeds the {settings.MAX_PLUGIN_SIZE_MB}MB limit"
        )

    try:

        wasmtime.Module.validate(_validation_engine, content)

    except wasmtime.WasmtimeError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not a valid WebAssembly module: {exc}"
        )

    return content


@router.post("", response_model=PluginOut, status_code=status.HTTP_201_CREATED)
async def create_plugin(
    name: str = Form(...),
    description: str | None = Form(default=None),
    version: str = Form(default="1.0.0"),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    content = await _read_and_validate_wasm(file)

    storage_dir = _owner_storage_dir(current_user.id)
    stored_filename = f"{uuid.uuid4()}.wasm"
    file_path = os.path.join(storage_dir, stored_filename)

    with open(file_path, "wb") as f:

        f.write(content)

    plugin = Plugin(
        name=name,
        description=description,
        filename=file.filename,
        file_path=file_path,
        version=version,
        owner_id=current_user.id
    )

    db.add(plugin)
    db.commit()
    db.refresh(plugin)

    return plugin


@router.get("", response_model=list[PluginOut])
def list_plugins(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(Plugin).filter(Plugin.owner_id == current_user.id).order_by(Plugin.created_at.desc()).all()


@router.get("/{plugin_id}", response_model=PluginOut)
def get_plugin(
    plugin_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return _get_owned_plugin(plugin_id, current_user, db)


@router.put("/{plugin_id}", response_model=PluginOut)
def update_plugin(
    plugin_id: str,
    payload: PluginUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    plugin = _get_owned_plugin(plugin_id, current_user, db)

    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():

        setattr(plugin, field, value)

    db.commit()
    db.refresh(plugin)

    return plugin


@router.delete("/{plugin_id}", status_code=status.HTTP_200_OK)
def delete_plugin(
    plugin_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    plugin = _get_owned_plugin(plugin_id, current_user, db)

    if os.path.exists(plugin.file_path):

        os.remove(plugin.file_path)

    db.delete(plugin)
    db.commit()

    return success(messages.PLUGIN_DELETED)


@router.post("/{plugin_id}/execute", response_model=ExecuteResponse)
def run_plugin(
    plugin_id: str,
    payload: ExecuteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    plugin = _get_owned_plugin(plugin_id, current_user, db)

    if not plugin.is_active:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plugin is inactive"
        )

    return execute_plugin(
        wasm_path=plugin.file_path,
        function=payload.function,
        args=payload.args,
        stdin_text=payload.stdin
    )
