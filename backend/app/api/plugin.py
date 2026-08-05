from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
    UploadFile,
    File,
    Form,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User

from app.schemas.plugin import (
    PluginCreate,
    PluginUpdate,
    PluginResponse,
    PluginListResponse,
    PluginSearchQuery,
    PluginImport,
)

from app.services.plugin_service import plugin_service

router = APIRouter(
    prefix="/plugins",
    tags=["Plugins"],
)


# =====================================================
# Create Plugin (Compile Source Code)
# =====================================================

@router.post(
    "/",
    response_model=PluginResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_plugin(
    plugin: PluginCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return plugin_service.create_plugin(
        db=db,
        plugin=plugin,
        user_id=current_user.id,
    )


# =====================================================
# Import Existing WASM Plugin
# =====================================================

@router.post(
    "/import",
    response_model=PluginResponse,
    status_code=status.HTTP_201_CREATED,
)
def import_plugin(
    name: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plugin = PluginImport(
        name=name,
        description=description,
    )

    return plugin_service.import_plugin(
        db=db,
        plugin=plugin,
        file=file,
        user_id=current_user.id,
    )


# =====================================================
# Get All Plugins
# =====================================================

@router.get(
    "/",
    response_model=PluginListResponse,
)
def get_plugins(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),

    search: str | None = Query(None),
    language: str | None = Query(None),
    status: str | None = Query(None),

    # -----------------------------
    # NEW FILTERS
    # -----------------------------
    category: str | None = Query(None),
    tag: str | None = Query(None),

    sort: str = Query("created_at"),
    order: str = Query("desc"),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    query = PluginSearchQuery(
        page=page,
        limit=limit,
        search=search,
        language=language,
        status=status,
        category=category,
        tag=tag,
        sort=sort,
        order=order,
    )

    return plugin_service.get_plugins(
        db=db,
        user_id=current_user.id,
        query=query,
    )


# =====================================================
# Get Single Plugin
# =====================================================

@router.get(
    "/{plugin_id}",
    response_model=PluginResponse,
)
def get_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return plugin_service.get_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )


# =====================================================
# Download WASM
# =====================================================

@router.get(
    "/{plugin_id}/download",
)
def download_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    wasm_path, filename = plugin_service.download_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )

    return FileResponse(
        path=wasm_path,
        filename=filename,
        media_type="application/wasm",
    )


# =====================================================
# Update Plugin
# =====================================================

@router.put(
    "/{plugin_id}",
    response_model=PluginResponse,
)
def update_plugin(
    plugin_id: str,
    plugin: PluginUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return plugin_service.update_plugin(
        db=db,
        plugin_id=plugin_id,
        plugin_data=plugin,
        user_id=current_user.id,
    )


# =====================================================
# Delete Plugin
# =====================================================

@router.delete(
    "/{plugin_id}",
)
def delete_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return plugin_service.delete_plugin(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
    )