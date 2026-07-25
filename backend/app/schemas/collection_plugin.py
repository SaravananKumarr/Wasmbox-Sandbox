from uuid import UUID

from pydantic import BaseModel


class CollectionPluginCreate(BaseModel):
    plugin_id: UUID