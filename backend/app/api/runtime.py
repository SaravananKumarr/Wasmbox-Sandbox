from fastapi import APIRouter, HTTPException

from app.wasm.runtime import run_trusted_self_check

router = APIRouter()


@router.get("/runtime/self-check")
def runtime_self_check():
    try:
        return run_trusted_self_check()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Wasmtime runtime unavailable: {exc}") from exc
