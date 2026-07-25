from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.schemas.collection import (
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
)
from app.schemas.collection_plugin import CollectionPluginCreate
from app.services.collection_service import CollectionService
from app.dependencies.current_user import get_current_user

router = APIRouter(
    prefix="/collections",
    tags=["Collections"],
)


@router.post(
    "",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_collection(
    data: CollectionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return CollectionService.create_collection(
        db,
        data,
        current_user.id,
    )


@router.get(
    "",
    response_model=list[CollectionResponse],
)
def get_my_collections(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return CollectionService.get_my_collections(
        db,
        current_user.id,
    )


@router.get(
    "/{collection_id}",
    response_model=CollectionResponse,
)
def get_collection(
    collection_id: str,
    db: Session = Depends(get_db),
):
    try:
        return CollectionService.get_collection(
            db,
            collection_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.put(
    "/{collection_id}",
    response_model=CollectionResponse,
)
def update_collection(
    collection_id: str,
    data: CollectionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return CollectionService.update_collection(
            db,
            collection_id,
            data,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.delete(
    "/{collection_id}",
)
def delete_collection(
    collection_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        CollectionService.delete_collection(
            db,
            collection_id,
            current_user.id,
        )

        return {
            "message": "Collection deleted successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.post(
    "/{collection_id}/plugins",
)
def add_plugin(
    collection_id: str,
    data: CollectionPluginCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        CollectionService.add_plugin(
            db,
            collection_id,
            data,
            current_user.id,
        )

        return {
            "message": "Plugin added successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.delete(
    "/{collection_id}/plugins/{plugin_id}",
)
def remove_plugin(
    collection_id: str,
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        CollectionService.remove_plugin(
            db,
            collection_id,
            plugin_id,
            current_user.id,
        )

        return {
            "message": "Plugin removed successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.get(
    "/{collection_id}/plugins",
)
def get_collection_plugins(
    collection_id: str,
    db: Session = Depends(get_db),
):
    try:
        return CollectionService.get_collection_plugins(
            db,
            collection_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )