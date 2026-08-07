from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import time
import uuid

from app.database.dependency import get_db
from app.services.execution_service import run_execution
from app.compiler.compiler_service import compiler_service
from app.sandbox.executor import sandbox_executor


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


class CompileRunRequest(BaseModel):
    code: str
    language: str
    input: str = "{}"


@router.post("/compile-run")
def compile_and_run(
    body: CompileRunRequest,
    db: Session = Depends(get_db),
):
    """Compile source code to WASM (when supported) then execute it.

    Supported languages depend on `compiler_service` (e.g. `rust`). The
    endpoint returns an execution-like result so the frontend can reuse
    the same UI contract as `/executions`.
    """
    run_id = str(uuid.uuid4())

    # Save source to disk
    try:
        source_path = compiler_service.save_plugin(body.code, body.language)
    except Exception as exc:
        return {
            "id": run_id,
            "status": "Failed",
            "returnCode": 1,
            "duration": 0,
            "memory": 0.0,
            "output": None,
            "logs": [f"[ERROR] Failed to save source: {str(exc)}"],
        }

    # Compile to wasm
    compile_start = time.perf_counter()
    try:
        wasm_path = compiler_service.compile(source_path)
    except Exception as exc:
        compile_duration_ms = round((time.perf_counter() - compile_start) * 1000, 1)
        return {
            "id": run_id,
            "status": "Failed",
            "returnCode": 1,
            "duration": compile_duration_ms,
            "memory": 0.0,
            "output": None,
            "logs": [f"[ERROR] Compilation failed: {str(exc)}"],
        }

    compile_duration_ms = round((time.perf_counter() - compile_start) * 1000, 1)

    # Execute the generated WASM
    exec_start = time.perf_counter()
    exec_result = sandbox_executor.execute(wasm_path, body.input)
    exec_duration_ms = round((time.perf_counter() - exec_start) * 1000, 1)

    status = "Success" if exec_result.get("status") in ("success", "Success") else "Failed"
    return {
        "id": run_id,
        "status": status,
        "returnCode": 0 if status == "Success" else 1,
        "duration": round(compile_duration_ms + exec_duration_ms, 1),
        "memory": 0.0,
        "output": exec_result.get("stdout") or exec_result.get("stderr"),
        "logs": [f"[INFO] Compilation time: {compile_duration_ms} ms", f"[INFO] Execution time: {exec_duration_ms} ms"] + ([exec_result.get("stdout")] if exec_result.get("stdout") else []) + ([exec_result.get("stderr")] if exec_result.get("stderr") else []),
    }
