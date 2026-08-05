from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.schemas.marketplace import (
    MarketplaceListResponse,
    MarketplaceResponse,
    MarketplaceUpdate,
)
from app.schemas.marketplace_search import MarketplaceSearchFilter
from app.schemas.marketplace_stats import MarketplaceStatsResponse
from app.services.marketplace_service import MarketplaceService

router = APIRouter(
    prefix="/marketplace",
    tags=["Marketplace"],
)


@router.post(
    "/publish/{plugin_id}",
    response_model=MarketplaceResponse,
)
def publish_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return MarketplaceService.publish_plugin(
            db,
            plugin_id,
            current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post(
    "/unpublish/{plugin_id}",
    response_model=MarketplaceResponse,
)
def unpublish_plugin(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return MarketplaceService.unpublish_plugin(
            db,
            plugin_id,
            current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get(
    "",
    response_model=MarketplaceListResponse,
)
def get_marketplace(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return MarketplaceService.get_marketplace(
        db,
        page,
        limit,
    )


@router.get(
    "/search",
    response_model=MarketplaceListResponse,
)
def search_marketplace(
    search: str | None = None,
    category: str | None = None,
    language: str | None = None,
    sort_by: str = "latest",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    filters = MarketplaceSearchFilter(
        search=search,
        category=category,
        language=language,
        sort_by=sort_by,
        page=page,
        limit=limit,
    )

    return MarketplaceService.search_plugins(
        db,
        filters,
    )


@router.get(
    "/stats",
    response_model=MarketplaceStatsResponse,
)
def get_marketplace_statistics(
    db: Session = Depends(get_db),
):
    return MarketplaceService.get_statistics(
        db,
    )


@router.get(
    "/featured",
    response_model=list[MarketplaceResponse],
)
def get_featured_plugins(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return MarketplaceService.get_featured_plugins(
        db,
        limit,
    )


@router.get(
    "/trending",
    response_model=list[MarketplaceResponse],
)
def get_trending_plugins(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return MarketplaceService.get_trending_plugins(
        db,
        limit,
    )


@router.patch(
    "/{plugin_id}",
    response_model=MarketplaceResponse,
)
def update_marketplace(
    plugin_id: str,
    data: MarketplaceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return MarketplaceService.update_marketplace(
            db,
            plugin_id,
            data,
            current_user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post(
    "/{plugin_id}/view",
    response_model=MarketplaceResponse,
)
def increment_view(
    plugin_id: str,
    db: Session = Depends(get_db),
):
    try:
        return MarketplaceService.increment_view(
            db,
            plugin_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/{plugin_id}/download",
    response_model=MarketplaceResponse,
)
def increment_download(
    plugin_id: str,
    db: Session = Depends(get_db),
):
    try:
        return MarketplaceService.increment_download(
            db,
            plugin_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))