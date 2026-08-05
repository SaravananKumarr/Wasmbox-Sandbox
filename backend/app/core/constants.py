APP_NAME = "WasmBox Sandbox"

API_VERSION = "v1"

API_PREFIX = "/api/v1"

DEFAULT_PLUGIN_CODE = (
    "# Write your WasmBox plugin code here\n"
    "print('Hello from WasmBox!')\n"
)

# Modules that are never allowed to be imported inside a sandboxed plugin.
# Blocks filesystem, network, process, and introspection escape routes.
BLOCKED_MODULES = {
    "os", "subprocess", "socket", "sys", "shutil", "ctypes", "importlib",
    "multiprocessing", "threading", "resource", "signal", "ftplib",
    "telnetlib", "smtplib", "http", "urllib", "requests", "pickle",
    "marshal", "code", "pty", "platform", "pathlib", "sqlite3",
    "webbrowser", "asyncio", "shelve", "tempfile", "glob", "fcntl",
}

# Builtins that are stripped from the sandbox namespace and rejected by the
# AST scanner, either because they perform I/O or because they allow dynamic
# attribute access that can bypass the static import/attribute checks
# (e.g. getattr(obj, "__subclasses__")).
BLOCKED_BUILTINS = {
    "open", "eval", "exec", "compile", "__import__", "input",
    "breakpoint", "exit", "quit", "getattr", "setattr", "delattr",
    "vars", "globals", "locals", "dir", "memoryview",
}

# Attribute names commonly used to climb the Python object graph out of a
# restricted-builtins sandbox (e.g. ().__class__.__mro__[-1].__subclasses__()).
BLOCKED_ATTRIBUTES = {
    "__import__", "__globals__", "__subclasses__", "__base__",
    "__bases__", "__mro__", "__builtins__", "__loader__", "__spec__",
    "__code__", "__closure__", "__func__",
}