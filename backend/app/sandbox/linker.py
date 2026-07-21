from wasmtime import Linker
from app.core.logger import logger


class SandboxLinker:
    def __init__(self):
        self.linker = Linker()

    def register_host_functions(self):
        # Whitelist only safe host functions
        allowed_functions = [
            "write_log",
            "save_user_data",
            "get_user_config",
        ]
        logger.info(f"Sandbox linker initialized. Allowed functions: {allowed_functions}")
        return allowed_functions

    def is_blocked(self, func_name: str) -> bool:
        blocked = ["filesystem", "network", "subprocess", "env_vars", "open", "socket", "fork"]
        return func_name in blocked
