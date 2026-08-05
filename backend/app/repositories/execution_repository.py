from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.execution import Execution


class ExecutionRepository:

    def create_execution(
        self,
        db: Session,
        plugin_id: str,
        status: str,
        output: str | None,
        error: str |None,
        execution_time: float,
    ):

        execution = Execution(
            plugin_id=plugin_id,
            status=status,
            output=output,
            error=error,
            execution_time=execution_time,
        )

        db.add(execution)
        db.commit()
        db.refresh(execution)

        return execution

    def get_execution(
        self,
        db: Session,
        execution_id: str,
    ):
        return (
            db.query(Execution)
            .filter(Execution.id == execution_id)
            .first()
        )

    def get_plugin_executions(
        self,
        db: Session,
        plugin_id: str,
    ):
        return (
            db.query(Execution)
            .filter(Execution.plugin_id == plugin_id)
            .order_by(Execution.created_at.desc())
            .all()
        )

    def count_total(
        self,
        db: Session,
        plugin_id: str,
    ):
        return (
            db.query(Execution)
            .filter(Execution.plugin_id == plugin_id)
            .count()
        )

    def count_success(
        self,
        db: Session,
        plugin_id: str,
    ):
        return (
            db.query(Execution)
            .filter(
                Execution.plugin_id == plugin_id,
                Execution.status == "success",
            )
            .count()
        )

    def count_failed(
        self,
        db: Session,
        plugin_id: str,
    ):
        return (
            db.query(Execution)
            .filter(
                Execution.plugin_id == plugin_id,
                Execution.status == "failed",
            )
            .count()
        )

    def average_execution_time(
        self,
        db: Session,
        plugin_id: str,
    ):
        avg = (
            db.query(func.avg(Execution.execution_time))
            .filter(Execution.plugin_id == plugin_id)
            .scalar()
        )

        return float(avg or 0)

    def latest_execution(
        self,
        db: Session,
        plugin_id: str,
    ):
        return (
            db.query(Execution)
            .filter(Execution.plugin_id == plugin_id)
            .order_by(Execution.created_at.desc())
            .first()
        )


execution_repository = ExecutionRepository()