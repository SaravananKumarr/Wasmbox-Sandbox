from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Base
# ==========================================

class CommentBase(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Comment content",
    )


# ==========================================
# Create Comment
# ==========================================

class CommentCreate(CommentBase):
    parent_id: Optional[str] = None


# ==========================================
# Update Comment
# ==========================================

class CommentUpdate(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


# ==========================================
# Response
# ==========================================

class CommentResponse(BaseModel):
    id: str
    plugin_id: str
    user_id: str
    parent_id: Optional[str]
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================
# Nested Reply Response
# ==========================================

class CommentTreeResponse(CommentResponse):
    replies: list["CommentTreeResponse"] = []


CommentTreeResponse.model_rebuild()