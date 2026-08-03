from typing import Optional

from pydantic import BaseModel


class ExecuteRequest(BaseModel):

    plugin_id: Optional[str] = None

    code: str

    input: str = "{}"
