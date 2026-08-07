from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.services.execution_service import run_execution

router = APIRouter(
    prefix="/sandbox",
    tags=["Sandbox"],
)


class RunRequest(BaseModel):
    code: str
    input: str = "{}"


@router.post("/run")
def run_code(
    body: RunRequest,
    db: Session = Depends(get_db),
):
    """Run arbitrary plugin source inside the backend sandbox.

    This endpoint is intentionally unauthenticated to support the local
    editor/preview UX. It validates and executes the provided `code`
    using the same sandbox engine as authenticated executions.
    """
    result = run_execution(db, body.code, body.input)
    return result
