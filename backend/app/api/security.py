from fastapi import APIRouter

from app.core.config import settings
from app.core.constants import BLOCKED_BUILTINS, BLOCKED_MODULES

router = APIRouter()


@router.get("/security/policy")
def get_security_policy():
    """Return the effective, read-only sandbox policy for the UI and audits."""
    return {
        "runtime": "Restricted Python subprocess",
        "wasmRuntime": "Wasmtime (trusted-module self-check only)",
        "pythonCompilerAvailable": False,
        "mode": "demo",
        "networkAccess": False,
        "filesystemAccess": False,
        "environmentAccess": False,
        "hostFunctions": False,
        "memoryLimitMb": settings.SANDBOX_MEMORY_MB,
        "cpuLimitSeconds": settings.SANDBOX_CPU_SECONDS,
        "timeoutSeconds": settings.SANDBOX_TIMEOUT_SECONDS,
        "blockedModuleCount": len(BLOCKED_MODULES),
        "blockedBuiltinCount": len(BLOCKED_BUILTINS),
        "notice": "This is a development demonstration. It is not a WebAssembly runtime and must not be used as a production-grade isolation boundary.",
    }
