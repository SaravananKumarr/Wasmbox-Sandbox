import time
from sqlalchemy.orm import Session

from app.models.plugin import Plugin
from app.repositories.execution_repository import execution_repository
from app.sandbox.executor import sandbox_executor


class ExecutionService:

    def execute_plugin(
        self,
        db: Session,
        plugin: Plugin,
        stdin: str | None = None,
    ):

        start = time.perf_counter()

        result = sandbox_executor.execute(
            plugin.wasm_path,
            stdin,
        )

        execution_time = time.perf_counter() - start

        return execution_repository.create_execution(
            db=db,
            plugin_id=plugin.id,
            status=result["status"],
            output=result.get("stdout"),
            error=result.get("stderr"),
            execution_time=execution_time,
        )

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

        success_rate = 0

        if total > 0:
            success_rate = round((success / total) * 100, 2)

        return {
            "plugin_id": plugin_id,
            "total_executions": total,
            "successful_executions": success,
            "failed_executions": failed,
            "average_execution_time": round(avg, 6),
            "success_rate": success_rate,
            "latest_execution": latest,
        }


execution_service = ExecutionService()