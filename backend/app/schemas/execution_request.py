from pydantic import BaseModel


class ExecutionRequest(BaseModel):
    stdin: str | None = None