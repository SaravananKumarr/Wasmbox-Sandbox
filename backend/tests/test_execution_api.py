import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.api.execution import RunRequest, run_plugin


def test_run_response_uses_consistent_snake_case_names():
    body = run_plugin(RunRequest(code="print('API contract')", input="{}"))

    assert body["status"] == "Success"
    assert body["return_code"] == 0
    assert body["duration_ms"] >= 0
    assert body["memory_mb"] >= 0
    assert body["output"] == "API contract"
    assert body["error_message"] is None
    assert body["resource_usage"] == {
        "duration_ms": body["duration_ms"],
        "memory_mb": body["memory_mb"],
        "fuel_consumed": None,
    }
    assert body["resource_limits"]["execution_timeout_ms"] == 50
    assert body["resource_limits"]["sandbox_memory_mb"] == 128
    assert body["resource_limits"]["wasm_memory_mb"] == 10
    assert body["resource_limits"]["wasm_fuel"] == 100000
    assert "returnCode" not in body
