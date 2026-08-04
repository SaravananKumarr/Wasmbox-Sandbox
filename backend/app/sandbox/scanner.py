import ast

from app.core.constants import BLOCKED_ATTRIBUTES
from app.core.constants import BLOCKED_BUILTINS
from app.core.constants import BLOCKED_MODULES


def scan_code(code: str) -> list[str]:
    """Statically inspect plugin source for restricted imports, calls and
    attribute access. Returns a list of human-readable violations; an empty
    list means the code passed the security scan.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return [f"SyntaxError: {exc.msg} (line {exc.lineno})"]

    violations = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in BLOCKED_MODULES:
                    violations.append(
                        f"Blocked import '{alias.name}' at line {node.lineno}"
                    )

        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root in BLOCKED_MODULES:
                violations.append(
                    f"Blocked import '{node.module}' at line {node.lineno}"
                )

        elif isinstance(node, ast.Call):
            func = node.func
            name = func.id if isinstance(func, ast.Name) else None
            if name in BLOCKED_BUILTINS:
                violations.append(
                    f"Blocked call to '{name}()' at line {node.lineno}"
                )

        elif isinstance(node, ast.Attribute):
            if node.attr in BLOCKED_ATTRIBUTES or (node.attr.startswith("__") and node.attr.endswith("__")):
                violations.append(
                    f"Blocked attribute access '.{node.attr}' at line {node.lineno}"
                )

    return violations
