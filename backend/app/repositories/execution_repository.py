from sqlalchemy.orm import Session

from app.models.execution import Execution


class ExecutionRepository:
    """
    Repository responsible for Execution database operations.
    """

    def create_execution(
        self,
        db: Session,
        execution: Execution,
    ) -> Execution:

        db.add(execution)
        db.commit()
        db.refresh(execution)

        return execution

    def get_execution(
        self,
        db: Session,
        execution_id: str,
    ) -> Execution | None:

        return (
            db.query(Execution)
            .filter(Execution.id == execution_id)
            .first()
        )

    def get_plugin_executions(
        self,
        db: Session,
        plugin_id: str,
    ) -> list[Execution]:

        return (
            db.query(Execution)
            .filter(Execution.plugin_id == plugin_id)
            .order_by(Execution.created_at.desc())
            .all()
        )


execution_repository = ExecutionRepository()