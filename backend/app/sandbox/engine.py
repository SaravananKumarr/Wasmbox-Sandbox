import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

from app.core.config import settings
from app.sandbox.scanner import scan_code

ENTRYPOINT = Path(__file__).parent / "_entrypoint.py"
RESULT_MARKER = "__WASMBOX_RESULT__"

_active_lock = threading.Lock()
_active_count = 0


def get_active_sandbox_count() -> int:
    """Number of plugin executions currently running inside this backend
    process. A real value (not fabricated), scoped to a single worker.
    """
    with _active_lock:
        return _active_count


def _limit_resources():
    """Runs in the child process (POSIX only) right before exec, via
    subprocess's preexec_fn. Caps CPU time and address space so a runaway
    or malicious plugin can't starve the host.
    """
    import resource

    cpu_seconds = settings.SANDBOX_CPU_SECONDS
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))

    mem_bytes = settings.SANDBOX_MEMORY_MB * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
    except (ValueError, OSError):
        # RLIMIT_AS isn't enforceable in every environment (e.g. some
        # containerized/macOS setups) - CPU + wall clock limits still apply.
        pass


def execute_plugin(code: str, input_payload: str = "{}") -> dict:
    """Runs plugin `code` inside an isolated, resource-limited subprocess
    after statically scanning it for restricted imports/calls. Returns a
    dict matching the frontend's execution result contract:
    {status, return_code, duration_ms, memory_mb, output, error_message, logs}
    """
    logs = ["[INFO] [WasmBox Sandbox] Scanning plugin source for restricted imports..."]

    violations = scan_code(code)
    if violations:
        logs.append(
            f"[ERROR] [WasmBox Sandbox] Security scan rejected plugin: {'; '.join(violations)}"
        )
        logs.append("[FATAL] Execution blocked before sandbox launch")
        return {
            "status": "Failed",
            "return_code": 126,
            "duration_ms": 0.0,
            "memory_mb": 0.0,
            "output": f"SecurityError: {violations[0]}",
            "error_message": "; ".join(violations),
            "logs": logs,
        }

    logs.append(
        "[INFO] [WasmBox Sandbox] Initializing restricted subprocess "
        f"(CPU: {settings.SANDBOX_CPU_SECONDS}s, Memory: {settings.SANDBOX_MEMORY_MB}MB, "
        f"Wall clock: {settings.SANDBOX_TIMEOUT_SECONDS}s)"
    )
    logs.append("[INFO] [WasmBox Sandbox] Executing plugin in isolated namespace...")

    payload = json.dumps({"code": code, "input": input_payload})
    start = time.perf_counter()

    global _active_count
    with _active_lock:
        _active_count += 1

    try:
        try:
            proc = subprocess.run(
                [sys.executable, "-I", str(ENTRYPOINT)],
                input=payload,
                capture_output=True,
                text=True,
                timeout=settings.SANDBOX_TIMEOUT_SECONDS,
                preexec_fn=_limit_resources if os.name == "posix" else None,
            )
        except subprocess.TimeoutExpired:
            duration_ms = round((time.perf_counter() - start) * 1000, 1)
            logs.append(
                f"[ERROR] [WasmBox Sandbox] Execution exceeded wall-clock limit of "
                f"{settings.SANDBOX_TIMEOUT_SECONDS}s"
            )
            logs.append("[FATAL] Sandbox execution terminated (timeout)")
            return {
                "status": "Failed",
                "return_code": 124,
                "duration_ms": duration_ms,
                "memory_mb": 0.0,
                "output": f"TimeoutError: Execution exceeded {settings.SANDBOX_TIMEOUT_SECONDS}s wall-clock limit",
                "error_message": "Execution timed out",
                "logs": logs,
            }
    finally:
        with _active_lock:
            _active_count -= 1

    duration_ms = round((time.perf_counter() - start) * 1000, 1)

    stdout = proc.stdout or ""
    marker_idx = stdout.rfind(RESULT_MARKER)

    if marker_idx == -1:
        logs.append(
            "[ERROR] [WasmBox Sandbox] Sandbox process exited without a result "
            "(likely killed for exceeding CPU/memory limits)"
        )
        logs.append(f"[FATAL] Execution halted with return code {proc.returncode}")
        return {
            "status": "Failed",
            "return_code": proc.returncode if proc.returncode != 0 else 137,
            "duration_ms": duration_ms,
            "memory_mb": 0.0,
            "output": (proc.stderr or "Sandbox process terminated unexpectedly").strip()[:4000],
            "error_message": "Sandbox process produced no result",
            "logs": logs,
        }

    try:
        result = json.loads(stdout[marker_idx + len(RESULT_MARKER):])
    except json.JSONDecodeError:
        result = {"success": False, "stdout": "", "error": "Malformed sandbox response", "error_type": "InternalError"}

    memory_mb = result.get("memory_mb", 0.0)
    plugin_stdout = result.get("stdout", "")
    for line in plugin_stdout.splitlines():
        if line.strip():
            logs.append(f"[LOG] {line}")

    if result.get("success"):
        logs.append(
            f"[INFO] [WasmBox Sandbox] Execution completed successfully in "
            f"{duration_ms} ms (Memory peak: {memory_mb} MB)"
        )
        return {
            "status": "Success",
            "return_code": 0,
            "duration_ms": duration_ms,
            "memory_mb": memory_mb,
            "output": plugin_stdout.strip() or "(no output)",
            "error_message": None,
            "logs": logs,
        }

    error_type = result.get("error_type") or "Error"
    error_msg = result.get("error") or "Unknown error"
    logs.append(f"[ERROR] [WasmBox Sandbox] {error_type}: {error_msg}")
    logs.append("[FATAL] Plugin execution raised an exception")
    return {
        "status": "Failed",
        "return_code": 1,
        "duration_ms": duration_ms,
        "memory_mb": memory_mb,
        "output": f"{error_type}: {error_msg}",
        "error_message": f"{error_type}: {error_msg}",
        "logs": logs,
    }
