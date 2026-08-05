import time

from sqlalchemy.orm import Session

from app.models.plugin import Plugin
from app.repositories.execution_repository import execution_repository
from app.sandbox.executor import sandbox_executor
from app.services.execution_log_service import ExecutionLogService


class ExecutionService:

    def execute_plugin(
        self,
        db: Session,
        plugin: Plugin,
        stdin: str | None = None,
    ):
        start = time.perf_counter()

        try:
            result = sandbox_executor.execute(
                plugin.wasm_path,
                stdin,
            )

            execution_time = time.perf_counter() - start

            execution = execution_repository.create_execution(
                db=db,
                plugin_id=plugin.id,
                status=result["status"],
                output=result.get("stdout"),
                error=result.get("stderr"),
                execution_time=execution_time,
            )

            try:
                ExecutionLogService.create_log(
                    db=db,
                    plugin_id=plugin.id,
                    status=result["status"],
                    stdout=result.get("stdout"),
                    stderr=result.get("stderr"),
                    exit_code=result.get("exit_code", 0),
                    duration=execution_time,
                    memory_used=result.get("memory_used"),
                )
            except Exception as log_error:
                print(f"Execution log error: {log_error}")

            return execution

        except Exception as exc:
            execution_time = time.perf_counter() - start

            execution = execution_repository.create_execution(
                db=db,
                plugin_id=plugin.id,
                status="failed",
                output=None,
                error=str(exc),
                execution_time=execution_time,
            )

            try:
                ExecutionLogService.create_log(
                    db=db,
                    plugin_id=plugin.id,
                    status="failed",
                    stdout=None,
                    stderr=str(exc),
                    exit_code=1,
                    duration=execution_time,
                    memory_used=None,
                )
            except Exception as log_error:
                print(f"Execution log error: {log_error}")

            raise

    def get_history(
        self,
        db: Session,
        plugin_id: str,
    ):
        return execution_repository.get_plugin_executions(
            db=db,
            plugin_id=plugin_id,
        )

    def get_stats(
        self,
        db: Session,
        plugin_id: str,
    ):
        total = execution_repository.count_total(
            db,
            plugin_id,
        )

        success = execution_repository.count_success(
            db,
            plugin_id,
        )

        failed = execution_repository.count_failed(
            db,
            plugin_id,
        )

        avg = execution_repository.average_execution_time(
            db,
            plugin_id,
        )

        latest = execution_repository.latest_execution(
            db,
            plugin_id,
        )

        success_rate = (
            round((success / total) * 100, 2)
            if total > 0
            else 0
        )

        return {
            "plugin_id": plugin_id,
            "total_executions": total,
            "successful_executions": success,
            "failed_executions": failed,
            "average_execution_time": round(avg or 0, 6),
            "success_rate": success_rate,
            "latest_execution": latest,
        }


execution_service = ExecutionService()