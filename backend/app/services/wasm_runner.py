import os
import tempfile
import threading
import time

import wasmtime

from app.core.config import settings
from app.schemas.plugin import ExecuteResponse


def _build_engine() -> wasmtime.Engine:

    config = wasmtime.Config()
    config.consume_fuel = True
    config.epoch_interruption = True

    return wasmtime.Engine(config)


def _build_store(engine: wasmtime.Engine) -> wasmtime.Store:

    store = wasmtime.Store(engine)
    store.set_fuel(settings.WASM_FUEL_LIMIT)
    store.set_limits(memory_size=settings.WASM_MAX_MEMORY_MB * 1024 * 1024)
    store.set_epoch_deadline(1)

    return store


def _arm_timeout(engine: wasmtime.Engine) -> threading.Timer:

    timer = threading.Timer(settings.WASM_TIMEOUT_SECONDS, engine.increment_epoch)
    timer.daemon = True
    timer.start()

    return timer


def _fuel_consumed(store: wasmtime.Store) -> int:

    return settings.WASM_FUEL_LIMIT - store.get_fuel()


def run_function(wasm_path: str, function: str, args: list) -> ExecuteResponse:
    """Instantiate the module and call one of its exported functions directly."""

    engine = _build_engine()
    start = time.monotonic()

    try:

        module = wasmtime.Module.from_file(engine, wasm_path)

    except wasmtime.WasmtimeError as exc:

        return ExecuteResponse(
            success=False,
            mode="function",
            error=f"Invalid WebAssembly module: {exc}",
            execution_time_ms=(time.monotonic() - start) * 1000
        )

    store = _build_store(engine)
    timeout_timer = _arm_timeout(engine)

    try:

        linker = wasmtime.Linker(engine)
        instance = linker.instantiate(store, module)
        exports = instance.exports(store)

        target = exports.get(function)

        if target is None:

            return ExecuteResponse(
                success=False,
                mode="function",
                error=f"Export '{function}' was not found in this module",
                execution_time_ms=(time.monotonic() - start) * 1000
            )

        if not isinstance(target, wasmtime.Func):

            return ExecuteResponse(
                success=False,
                mode="function",
                error=f"Export '{function}' is not a callable function",
                execution_time_ms=(time.monotonic() - start) * 1000
            )

        return_value = target(store, *args)

        return ExecuteResponse(
            success=True,
            mode="function",
            return_value=return_value,
            execution_time_ms=(time.monotonic() - start) * 1000,
            fuel_consumed=_fuel_consumed(store)
        )

    except wasmtime.Trap as trap:

        return ExecuteResponse(
            success=False,
            mode="function",
            error=f"Execution trapped: {trap}",
            execution_time_ms=(time.monotonic() - start) * 1000,
            fuel_consumed=_fuel_consumed(store)
        )

    except wasmtime.WasmtimeError as exc:

        return ExecuteResponse(
            success=False,
            mode="function",
            error=str(exc),
            execution_time_ms=(time.monotonic() - start) * 1000
        )

    finally:

        timeout_timer.cancel()
        store.close()
        engine.close()


def run_wasi(wasm_path: str, stdin_text: str | None = None) -> ExecuteResponse:
    """Instantiate the module as a WASI command and run its `_start` entrypoint."""

    engine = _build_engine()
    start = time.monotonic()

    try:

        module = wasmtime.Module.from_file(engine, wasm_path)

    except wasmtime.WasmtimeError as exc:

        return ExecuteResponse(
            success=False,
            mode="wasi",
            error=f"Invalid WebAssembly module: {exc}",
            execution_time_ms=(time.monotonic() - start) * 1000
        )

    store = _build_store(engine)
    timeout_timer = _arm_timeout(engine)

    stdout_file = tempfile.NamedTemporaryFile(delete=False, suffix=".stdout")
    stderr_file = tempfile.NamedTemporaryFile(delete=False, suffix=".stderr")
    stdout_file.close()
    stderr_file.close()

    stdin_path = None

    if stdin_text is not None:

        stdin_fd, stdin_path = tempfile.mkstemp(suffix=".stdin")

        with os.fdopen(stdin_fd, "w") as f:

            f.write(stdin_text)

    try:

        wasi_config = wasmtime.WasiConfig()
        wasi_config.argv = ["plugin"]
        wasi_config.stdout_file = stdout_file.name
        wasi_config.stderr_file = stderr_file.name

        if stdin_path is not None:

            wasi_config.stdin_file = stdin_path

        store.set_wasi(wasi_config)

        linker = wasmtime.Linker(engine)
        linker.define_wasi()
        instance = linker.instantiate(store, module)
        exports = instance.exports(store)

        start_func = exports.get("_start")

        if not isinstance(start_func, wasmtime.Func):

            return ExecuteResponse(
                success=False,
                mode="wasi",
                error="Module does not export a WASI '_start' entrypoint",
                execution_time_ms=(time.monotonic() - start) * 1000
            )

        error = None

        try:

            start_func(store)

        except wasmtime.Trap as trap:

            error = f"Execution trapped: {trap}"

        elapsed = (time.monotonic() - start) * 1000

        with open(stdout_file.name, "r", errors="replace") as f:

            stdout = f.read()

        with open(stderr_file.name, "r", errors="replace") as f:

            stderr = f.read()

        return ExecuteResponse(
            success=error is None,
            mode="wasi",
            stdout=stdout,
            stderr=stderr,
            error=error,
            execution_time_ms=elapsed,
            fuel_consumed=_fuel_consumed(store)
        )

    except wasmtime.WasmtimeError as exc:

        return ExecuteResponse(
            success=False,
            mode="wasi",
            error=str(exc),
            execution_time_ms=(time.monotonic() - start) * 1000
        )

    finally:

        timeout_timer.cancel()
        store.close()
        engine.close()

        os.unlink(stdout_file.name)
        os.unlink(stderr_file.name)

        if stdin_path is not None:

            os.unlink(stdin_path)


def execute_plugin(
    wasm_path: str,
    function: str | None = None,
    args: list | None = None,
    stdin_text: str | None = None
) -> ExecuteResponse:

    if function:

        return run_function(wasm_path, function, args or [])

    return run_wasi(wasm_path, stdin_text)
