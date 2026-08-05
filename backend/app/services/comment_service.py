from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.comment_repository import comment_repository
from app.repositories.plugin_repository import plugin_repository
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
)


class CommentService:
    """
    Business logic for Comment operations.
    """

    # ----------------------------------
    # Create Comment / Reply
    # ----------------------------------

    def create_comment(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
        comment: CommentCreate,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        # Validate parent comment if replying
        if comment.parent_id:

            parent = comment_repository.get_comment(
                db=db,
                comment_id=comment.parent_id,
            )

            if parent is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent comment not found.",
                )

            if str(parent.plugin_id) != str(plugin_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Parent comment belongs to another plugin.",
                )

        return comment_repository.create_comment(
            db=db,
            plugin_id=plugin_id,
            user_id=user_id,
            comment=comment,
        )

    # ----------------------------------
    # Get Plugin Comments
    # ----------------------------------

    def get_plugin_comments(
        self,
        db: Session,
        plugin_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        comments = comment_repository.get_plugin_comments(
            db=db,
            plugin_id=plugin_id,
            skip=skip,
            limit=limit,
        )

        return comments

    # ----------------------------------
    # Get Replies
    # ----------------------------------

    def get_replies(
        self,
        db: Session,
        comment_id: str,
    ):

        comment = comment_repository.get_comment(
            db=db,
            comment_id=comment_id,
        )

        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found.",
            )

        return comment_repository.get_replies(
            db=db,
            parent_id=comment_id,
        )

    # ----------------------------------
    # Update Comment
    # ----------------------------------

    def update_comment(
        self,
        db: Session,
        comment_id: str,
        user_id: str,
        comment: CommentUpdate,
    ):

        db_comment = comment_repository.get_comment(
            db=db,
            comment_id=comment_id,
        )

        if db_comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found.",
            )

        if str(db_comment.user_id) != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can edit only your own comments.",
            )

        return comment_repository.update_comment(
            db=db,
            db_comment=db_comment,
            comment=comment,
        )

    # ----------------------------------
    # Delete Comment
    # ----------------------------------

    def delete_comment(
        self,
        db: Session,
        comment_id: str,
        user_id: str,
    ):

        db_comment = comment_repository.get_comment(
            db=db,
            comment_id=comment_id,
        )

        if db_comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found.",
            )

        if str(db_comment.user_id) != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can delete only your own comments.",
            )

        comment_repository.delete_comment(
            db=db,
            db_comment=db_comment,
        )

        return {
            "message": "Comment deleted successfully."
        }

    # ----------------------------------
    # Comment Count
    # ----------------------------------

    def get_comment_count(
        self,
        db: Session,
        plugin_id: str,
    ):

        plugin = plugin_repository.get_plugin_by_id(
            db=db,
            plugin_id=plugin_id,
        )

        if plugin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plugin not found.",
            )

        return {
            "plugin_id": plugin_id,
            "total_comments": comment_repository.count_comments(
                db=db,
                plugin_id=plugin_id,
            ),
        }


comment_service = CommentService()