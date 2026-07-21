from sqlalchemy.orm import Session
import time
from app.models.plugin import Plugin, ExecutionLog
from app.sandbox.engine import SandboxEngine
from app.compiler.wasm_compiler import WasmCompiler
from app.sandbox.memory_guard import MemoryGuard
from app.sandbox.fuel_guard import FuelGuard


class ExecutionService:
    def __init__(self, db: Session):
        self.db = db
        self.engine = SandboxEngine()
        self.compiler = WasmCompiler()

    def run_from_source(self, source_code: str, owner: str) -> dict:
        try:
            plugin = Plugin(
                name="temp_run",
                owner=owner,
                source_code=source_code,
                is_public=False,
            )
            self.db.add(plugin)
            self.db.commit()
            self.db.refresh(plugin)

            # Phase 2: AST Security Scan
            from app.compiler.ast_scanner import ASTSecurityScanner
            scanner = ASTSecurityScanner()
            scan_result = scanner.scan(source_code)
            if scan_result.get("blocked"):
                log = ExecutionLog(
                    plugin_id=plugin.id,
                    stdout="",
                    stderr=f"Security blocked: {scan_result.get('reason')}",
                    status="blocked",
                    execution_time_ms=0.0,
                    memory_bytes=0,
                    fuel_consumed=0,
                )
                self.db.add(log)
                self.db.commit()
                return {"plugin_id": plugin.id, "status": "blocked", "message": scan_result.get("reason")}

            # Phase 3: Compile to WASM (simulated / practical approach)
            wasm_binary = self.compiler.compile(source_code)
            plugin.wasm_binary = wasm_binary
            plugin.execution_count += 1
            self.db.commit()

            # Phase 4: Sandbox execution
            result = self.engine.execute(wasm_binary, plugin.id, plugin.name)

            log = ExecutionLog(
                plugin_id=plugin.id,
                stdout=result.get("stdout", ""),
                stderr=result.get("stderr", ""),
                status=result.get("status", "completed"),
                execution_time_ms=result.get("execution_time_ms", 0.0),
                memory_bytes=result.get("memory_bytes", 0),
                fuel_consumed=result.get("fuel_consumed", 0),
            )
            self.db.add(log)
            self.db.commit()
            return {
                "plugin_id": plugin.id,
                "status": "completed",
                "stdout": result.get("stdout"),
                "stderr": result.get("stderr"),
                "execution_time_ms": result.get("execution_time_ms"),
                "memory_bytes": result.get("memory_bytes"),
                "fuel_consumed": result.get("fuel_consumed"),
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def trigger_by_id(self, plugin_id: str) -> dict:
        plugin = self.db.query(Plugin).filter(Plugin.id == plugin_id).first()
        if not plugin:
            return {"status": "error", "message": "Plugin not found"}
        plugin.execution_count += 1
        self.db.commit()
        result = self.engine.execute(plugin.wasm_binary, plugin.id, plugin.name)
        log = ExecutionLog(
            plugin_id=plugin.id,
            stdout=result.get("stdout", ""),
            stderr=result.get("stderr", ""),
            status=result.get("status", "completed"),
            execution_time_ms=result.get("execution_time_ms", 0.0),
            memory_bytes=result.get("memory_bytes", 0),
            fuel_consumed=result.get("fuel_consumed", 0),
        )
        self.db.add(log)
        self.db.commit()
        return {
            "plugin_id": plugin.id,
            "status": result.get("status"),
            "stdout": result.get("stdout"),
            "stderr": result.get("stderr"),
        }
