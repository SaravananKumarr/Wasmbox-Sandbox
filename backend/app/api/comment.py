from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User

from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse,
)

from app.services.comment_service import comment_service

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


# =====================================================
# Create Comment / Reply
# =====================================================

@router.post(
    "/{plugin_id}",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    plugin_id: str,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return comment_service.create_comment(
        db=db,
        plugin_id=plugin_id,
        user_id=current_user.id,
        comment=comment,
    )


# =====================================================
# Get Plugin Comments
# =====================================================

@router.get(
    "/{plugin_id}",
    response_model=list[CommentResponse],
)
def get_plugin_comments(
    plugin_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return comment_service.get_plugin_comments(
        db=db,
        plugin_id=plugin_id,
        skip=skip,
        limit=limit,
    )


# =====================================================
# Get Replies
# =====================================================

@router.get(
    "/reply/{comment_id}",
    response_model=list[CommentResponse],
)
def get_replies(
    comment_id: str,
    db: Session = Depends(get_db),
):
    return comment_service.get_replies(
        db=db,
        comment_id=comment_id,
    )


# =====================================================
# Update Comment
# =====================================================

@router.put(
    "/{comment_id}",
    response_model=CommentResponse,
)
def update_comment(
    comment_id: str,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return comment_service.update_comment(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id,
        comment=comment,
    )


# =====================================================
# Delete Comment
# =====================================================

@router.delete(
    "/{comment_id}",
)
def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return comment_service.delete_comment(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id,
    )


# =====================================================
# Comment Count
# =====================================================

@router.get(
    "/{plugin_id}/count",
)
def comment_count(
    plugin_id: str,
    db: Session = Depends(get_db),
):
    return comment_service.get_comment_count(
        db=db,
        plugin_id=plugin_id,
    )