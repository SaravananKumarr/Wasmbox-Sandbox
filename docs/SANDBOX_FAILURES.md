# Sandbox failure handling

The `POST /api/run` endpoint always returns a JSON execution result. A plugin
failure is represented in the response body; it does not cause the API to
return an unstructured server error.

## Response fields

| Field | Meaning |
| --- | --- |
| `status` | `Success` or `Failed` |
| `return_code` | `0` for success; `1` for a plugin error; `124` for timeout; `126` for a source-security rejection |
| `duration_ms` | Total observed execution duration in milliseconds |
| `memory_mb` | Observed peak memory when supported by the host platform |
| `output` | Plugin stdout on success, or a readable failure message |
| `error_message` | Detailed failure reason, or `null` on success |
| `logs` | Ordered diagnostic log messages for the editor console |

## Failure cases

### Source rejected before launch

Restricted imports and unsafe builtins are caught by the source scanner. The
API returns `status: "Failed"` and `return_code: 126`; the plugin is never
started.

### Syntax or runtime error

Invalid Python and exceptions raised by the plugin return `status: "Failed"`
and `return_code: 1`. The frontend displays the readable error from `output`
and preserves the diagnostic logs.

### Timeout

An execution that exceeds `SANDBOX_TIMEOUT_SECONDS` returns `return_code: 124`
and `error_message: "Execution timed out"`. Windows process startup time is
accounted for separately with `SANDBOX_STARTUP_GRACE_SECONDS`.

### Unexpected child-process exit

If the child runner exits without returning a result marker, the API returns a
failed response with the child process's exit code and captures stderr in
`output` when available.
