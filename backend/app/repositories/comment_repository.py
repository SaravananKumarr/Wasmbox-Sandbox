from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
)


class CommentRepository:

    # ----------------------------------
    # Create Comment
    # ----------------------------------

    def create_comment(
        self,
        db: Session,
        plugin_id: str,
        user_id: str,
        comment: CommentCreate,
    ) -> Comment:

        db_comment = Comment(
            plugin_id=plugin_id,
            user_id=user_id,
            parent_id=comment.parent_id,
            content=comment.content,
        )

        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)

        return db_comment

    # ----------------------------------
    # Get Comment By ID
    # ----------------------------------

    def get_comment(
        self,
        db: Session,
        comment_id: str,
    ) -> Comment | None:

        return (
            db.query(Comment)
            .filter(Comment.id == comment_id)
            .first()
        )

    # ----------------------------------
    # Get Plugin Comments
    # (Top-level comments only)
    # ----------------------------------

    def get_plugin_comments(
        self,
        db: Session,
        plugin_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return (
            db.query(Comment)
            .filter(
                Comment.plugin_id == plugin_id,
                Comment.parent_id.is_(None),
            )
            .order_by(Comment.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ----------------------------------
    # Get Replies
    # ----------------------------------

    def get_replies(
        self,
        db: Session,
        parent_id: str,
    ):

        return (
            db.query(Comment)
            .filter(Comment.parent_id == parent_id)
            .order_by(Comment.created_at.asc())
            .all()
        )

    # ----------------------------------
    # Update Comment
    # ----------------------------------

    def update_comment(
        self,
        db: Session,
        db_comment: Comment,
        comment: CommentUpdate,
    ) -> Comment:

        update_data = comment.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_comment, key, value)

        db.commit()
        db.refresh(db_comment)

        return db_comment

    # ----------------------------------
    # Delete Comment
    # ----------------------------------

    def delete_comment(
        self,
        db: Session,
        db_comment: Comment,
    ):

        db.delete(db_comment)
        db.commit()

    # ----------------------------------
    # Count Comments
    # ----------------------------------

    def count_comments(
        self,
        db: Session,
        plugin_id: str,
    ) -> int:

        return (
            db.query(func.count(Comment.id))
            .filter(Comment.plugin_id == plugin_id)
            .scalar()
        )


comment_repository = CommentRepository()