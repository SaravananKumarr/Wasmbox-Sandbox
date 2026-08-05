from pydantic import BaseModel


class PluginTagCreate(BaseModel):
    tag_id: str