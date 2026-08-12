import sys
from pathlib import Path
from unittest.mock import patch

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


def test_run_endpoint_returns_timeout_usage_and_limits_for_a_runaway_plugin():
    with patch("app.sandbox.engine.settings.SANDBOX_TIMEOUT_SECONDS", 0.05):
        body = run_plugin(RunRequest(code="while True:\n    pass", input="{}"))

    assert body["status"] == "Failed"
    assert body["return_code"] == 124
    assert body["error_message"] == "Execution timed out"
    assert body["resource_usage"]["duration_ms"] >= 50
    assert body["resource_usage"]["memory_mb"] == 0.0
    assert body["resource_limits"]["execution_timeout_ms"] == 50
