# Host-function contract

## Purpose

Wasm plugins have no host capabilities by default. The Wasmtime linker must
expose only the functions defined in `app.sandbox.host_contract`. Any name not
listed there must fail closed and must not be resolved by the host.

## Allowed functions

| Function | Arguments | Return | Rules |
| --- | --- | --- | --- |
| `write_log` | `level`, `message` | none | `level` is `info`, `warning`, or `error`; message is non-empty and at most 1,024 characters. |
| `get_input` | none | immutable execution input | Returns only the payload supplied with the current run. |

## Explicitly denied capabilities

The linker must not provide file access, network access, process execution,
environment-variable access, clocks, random sources, database connections, or
arbitrary host callbacks. WASI must remain unlinked unless a later reviewed
contract adds a specific capability.

## Linker implementation rules

1. Import `ALLOWED_HOST_FUNCTIONS` and call `validate_host_call` before a host
   callback handles arguments.
2. Define imports in a dedicated `wasmbox` module namespace.
3. Pass execution-scoped state only; never use global mutable state to share
   plugin data between tenants.
4. Convert host validation errors into controlled Wasm traps or structured
   execution errors. Do not leak stack traces or filesystem paths.
5. Log each accepted host call with the function name and plugin execution ID;
   do not log sensitive input payloads.

## Future changes

Adding a function requires a contract update, validation tests, linker tests,
and a security review. Do not add general-purpose functions such as filesystem
or HTTP wrappers; introduce a narrowly scoped operation instead.
