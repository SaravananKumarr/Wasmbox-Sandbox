from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ExecuteRequest(BaseModel):
    plugin_id: Optional[str] = None
    code: str
    input: str = "{}"


class ExecutionResponse(BaseModel):
    id: str
    plugin_id: str
    status: str
    output: str
    error: str
    execution_time: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)