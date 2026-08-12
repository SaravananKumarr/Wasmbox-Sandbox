import sys
from pathlib import Path

import pytest


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.sandbox.host_contract import ALLOWED_HOST_FUNCTIONS, validate_host_call


def test_contract_exposes_only_the_intended_host_functions():
    assert set(ALLOWED_HOST_FUNCTIONS) == {"write_log", "get_input"}


def test_write_log_accepts_a_bounded_diagnostic_message():
    function = validate_host_call("write_log", ("info", "plugin started"))

    assert function.name == "write_log"


def test_get_input_accepts_no_arguments():
    function = validate_host_call("get_input", ())

    assert function.name == "get_input"


def test_unlisted_host_function_is_rejected():
    with pytest.raises(PermissionError, match="not allowed"):
        validate_host_call("open_file", ("secret.txt",))


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        (("debug", "details"), "level"),
        (("info", ""), "non-empty"),
        (("info", "x" * 1_025), "must not exceed"),
        (("info",), "expects 2 arguments"),
    ],
)
def test_write_log_rejects_invalid_arguments(arguments, message):
    with pytest.raises(ValueError, match=message):
        validate_host_call("write_log", arguments)
