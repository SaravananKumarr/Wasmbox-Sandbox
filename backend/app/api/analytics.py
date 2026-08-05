from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.dependency import get_db

from app.schemas.analytics import (
    PluginAnalyticsResponse,
    DownloadTrendResponse,
    TopPluginResponse,
)

from app.services.analytics_service import analytics_service

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


# =====================================================
# Plugin Analytics Dashboard
# =====================================================

@router.get(
    "/plugin/{plugin_id}",
    response_model=PluginAnalyticsResponse,
)
def plugin_dashboard(
    plugin_id: str,
    db: Session = Depends(get_db),
):
    return analytics_service.get_plugin_analytics(
        db=db,
        plugin_id=plugin_id,
    )


# =====================================================
# Download Trend
# =====================================================

@router.get(
    "/plugin/{plugin_id}/downloads",
    response_model=DownloadTrendResponse,
)
def download_trend(
    plugin_id: str,
    db: Session = Depends(get_db),
):
    return analytics_service.get_download_trend(
        db=db,
        plugin_id=plugin_id,
    )


# =====================================================
# Top Rated Plugins
# =====================================================

@router.get(
    "/top-rated",
    response_model=list[TopPluginResponse],
)
def top_rated_plugins(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return analytics_service.get_top_rated_plugins(
        db=db,
        limit=limit,
    )


# =====================================================
# Most Downloaded Plugins
# =====================================================

@router.get(
    "/most-downloaded",
    response_model=list[TopPluginResponse],
)
def most_downloaded_plugins(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return analytics_service.get_most_downloaded_plugins(
        db=db,
        limit=limit,
    )