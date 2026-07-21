import ast
import sys
from app.core.logger import logger

BLOCKED_MODULES = {
    "os", "subprocess", "sys", "socket", "network", "urllib", "http",
    "ftplib", "smtplib", "poplib", "imaplib", "nntplib", "telnetlib",
    "pickle", "marshal", "ctypes", "mmap", "resource", "posix",
    "pwd", "grp", "crypt", "spwd", "shadow", "termios",
}

BLOCKED_BUILTINS = {
    "open", "eval", "exec", "compile", "__import__", "breakpoint",
}


class ASTSecurityScanner:
    def __init__(self):
        self.blocked = False
        self.reasons = []

    def scan(self, source_code: str) -> dict:
        try:
            tree = ast.parse(source_code)
        except Exception as e:
            return {"blocked": True, "reason": f"Invalid Python syntax: {e}"}

        for node in ast.walk(tree):
            # Module imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in BLOCKED_MODULES:
                        self.blocked = True
                        self.reasons.append(f"Blocked import: {alias.name}")
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                base = module.split(".")[0]
                if base in BLOCKED_MODULES:
                    self.blocked = True
                    self.reasons.append(f"Blocked import from: {module}")

            # Function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in BLOCKED_BUILTINS:
                    self.blocked = True
                    self.reasons.append(f"Blocked builtin call: {node.func.id}")
                if isinstance(node.func, ast.Attribute) and node.func.attr == "system":
                    self.blocked = True
                    self.reasons.append("Blocked os.system call")

        return {
            "blocked": self.blocked,
            "reason": "; ".join(self.reasons) if self.reasons else None,
        }
