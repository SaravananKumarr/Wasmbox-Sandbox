"""Deny-by-default contract for host functions exposed to Wasm plugins.

This module is intentionally independent from the Wasmtime linker. The linker
implementation should use this policy as its single source of truth.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class HostFunction:
    name: str
    argument_types: tuple[str, ...]
    description: str


ALLOWED_HOST_FUNCTIONS = {
    "write_log": HostFunction(
        name="write_log",
        argument_types=("level", "message"),
        description="Emit a bounded diagnostic log message for the current execution.",
    ),
    "get_input": HostFunction(
        name="get_input",
        argument_types=(),
        description="Read the immutable input payload supplied to the current execution.",
    ),
}

ALLOWED_LOG_LEVELS = frozenset({"info", "warning", "error"})
MAX_LOG_MESSAGE_LENGTH = 1_024


def validate_host_call(name: str, arguments: tuple[object, ...]) -> HostFunction:
    """Validate a proposed host call before it reaches a host implementation."""
    function = ALLOWED_HOST_FUNCTIONS.get(name)
    if function is None:
        raise PermissionError(f"Host function '{name}' is not allowed")

    if len(arguments) != len(function.argument_types):
        raise ValueError(
            f"Host function '{name}' expects {len(function.argument_types)} arguments"
        )

    if name == "write_log":
        level, message = arguments
        if level not in ALLOWED_LOG_LEVELS:
            raise ValueError("write_log level must be info, warning, or error")
        if not isinstance(message, str) or not message.strip():
            raise ValueError("write_log message must be a non-empty string")
        if len(message) > MAX_LOG_MESSAGE_LENGTH:
            raise ValueError(
                f"write_log message must not exceed {MAX_LOG_MESSAGE_LENGTH} characters"
            )

    return function
