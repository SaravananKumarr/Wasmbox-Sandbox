import wasmtime
import time
from app.core.logger import logger
from app.core.config import settings


class SandboxEngine:
    def __init__(self):
        self.engine = wasmtime.Engine()
        self.store = wasmtime.Store(self.engine)

    def execute(self, wasm_binary: bytes, plugin_id: str, plugin_name: str) -> dict:
        try:
            module = wasmtime.Module(wasmtime.Engine(), wasm_binary)
            instance = wasmtime.Instance(self.store, module, [])

            # Memory and fuel limits (Phase 4)
            from app.sandbox.memory_guard import MemoryGuard
            from app.sandbox.fuel_guard import FuelGuard
            MemoryGuard.enforce(instance, max_bytes=10 * 1024 * 1024)
            FuelGuard.enforce(instance, max_fuel=1_000_000)

            # Execute main if exists
            stdout = ""
            stderr = ""
            status = "completed"
            memory_bytes = 0
            fuel_consumed = 0
            execution_time_ms = 0.0

            if "main" in instance.exports(self.store):
                start = time.time()
                result = instance.exports(self.store)["main"](self.store)
                end = time.time()
                execution_time_ms = (end - start) * 1000
                stdout = f"Plugin {plugin_name} executed.\n"
                stderr = ""
            else:
                stdout = "No main function found in WASM module.\n"

            return {
                "stdout": stdout,
                "stderr": stderr,
                "status": status,
                "execution_time_ms": execution_time_ms,
                "memory_bytes": memory_bytes,
                "fuel_consumed": fuel_consumed,
            }
        except Exception as e:
            logger.error(f"Sandbox execution error: {e}")
            return {
                "stdout": "",
                "stderr": str(e),
                "status": "failed",
                "execution_time_ms": 0.0,
                "memory_bytes": 0,
                "fuel_consumed": 0,
            }
