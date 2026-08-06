"""Standalone entrypoint executed as an isolated subprocess by
app.sandbox.engine.execute_plugin(). Deliberately has no imports from the
rest of the app so it stays a minimal, auditable trust boundary: it reads a
{"code", "input"} JSON payload from stdin, runs it with a stripped-down
builtins namespace, and writes a single JSON result line to stdout prefixed
by a marker the parent process can locate.
"""
import builtins
import contextlib
import io
import json
import sys
try:
    import resource
except ImportError:
    resource = None
RESULT_MARKER = "__WASMBOX_RESULT__"

BLOCKED_BUILTINS = {
    "open", "eval", "exec", "compile", "__import__", "input",
    "breakpoint", "exit", "quit", "getattr", "setattr", "delattr",
    "vars", "globals", "locals", "dir", "memoryview",
}


def build_restricted_builtins():
    return {
        name: getattr(builtins, name)
        for name in dir(builtins)
        if name not in BLOCKED_BUILTINS
    }


def measure_peak_memory_mb():
    if resource is None:
        return 0.0
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    divisor = 1024 * 1024 if sys.platform == "darwin" else 1024
    return round(peak / divisor, 2)


def main():
    payload = json.loads(sys.stdin.read())
    code = payload["code"]
    input_payload = payload.get("input", "{}")

    namespace = {
        "__name__": "__wasmbox_plugin__",
        "__builtins__": build_restricted_builtins(),
        "INPUT": input_payload,
    }

    stdout_buffer = io.StringIO()
    result = {"success": True, "stdout": "", "error": None, "error_type": None}

    try:
        with contextlib.redirect_stdout(stdout_buffer):
            compiled = compile(code, "<plugin>", "exec")
            exec(compiled, namespace)
    except BaseException as exc:
        result["success"] = False
        result["error"] = str(exc)
        result["error_type"] = type(exc).__name__
    finally:
        result["stdout"] = stdout_buffer.getvalue()
        result["memory_mb"] = measure_peak_memory_mb()

    sys.stdout.write("\n" + RESULT_MARKER + json.dumps(result))


if __name__ == "__main__":
    main()
