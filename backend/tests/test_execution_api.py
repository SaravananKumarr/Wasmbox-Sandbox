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
    assert "returnCode" not in body
