import time

from sqlalchemy.orm import Session

from app.models.execution import Execution
from app.repositories.execution_repository import execution_repository
from app.sandbox.executor import sandbox_executor


class ExecutionService:
    """
    Handles plugin execution.
    """

    def execute_plugin(
        self,
        db: Session,
        plugin,
    ) -> Execution:

        start = time.perf_counter()

        result = sandbox_executor.execute(
            plugin.wasm_path,
        )

        elapsed = time.perf_counter() - start

        execution = Execution(
            plugin_id=plugin.id,
            status=result["status"],
            output=result["output"],
            error="",
            execution_time=f"{elapsed:.3f} sec",
        )

        return execution_repository.create_execution(
            db=db,
            execution=execution,
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


execution_service = ExecutionService()