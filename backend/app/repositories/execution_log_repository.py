from sqlalchemy.orm import Session

from app.models.execution_log import ExecutionLog
from app.schemas.execution_log import ExecutionLogFilter


class ExecutionLogRepository:

    @staticmethod
    def create(
        db: Session,
        execution_log: ExecutionLog,
    ) -> ExecutionLog:
        db.add(execution_log)
        db.commit()
        db.refresh(execution_log)
        return execution_log

    @staticmethod
    def get_by_id(
        db: Session,
        log_id: str,
    ) -> ExecutionLog | None:
        return (
            db.query(ExecutionLog)
            .filter(ExecutionLog.id == log_id)
            .first()
        )

    @staticmethod
    def get_plugin_logs(
        db: Session,
        plugin_id: str,
        filters: ExecutionLogFilter,
    ):
        query = (
            db.query(ExecutionLog)
            .filter(
                ExecutionLog.plugin_id == plugin_id
            )
        )

        if filters.status:
            query = query.filter(
                ExecutionLog.status == filters.status
            )

        total = query.count()

        logs = (
            query.order_by(
                ExecutionLog.executed_at.desc()
            )
            .offset(
                (filters.page - 1) * filters.limit
            )
            .limit(filters.limit)
            .all()
        )

        return total, logs

    @staticmethod
    def get_plugin_all_logs(
        db: Session,
        plugin_id: str,
    ) -> list[ExecutionLog]:
        return (
            db.query(ExecutionLog)
            .filter(
                ExecutionLog.plugin_id == plugin_id
            )
            .order_by(
                ExecutionLog.executed_at.desc()
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        execution_log: ExecutionLog,
    ) -> None:
        db.delete(execution_log)
        db.commit()

    @staticmethod
    def count_logs(
        db: Session,
        plugin_id: str,
    ) -> int:
        return (
            db.query(ExecutionLog)
            .filter(
                ExecutionLog.plugin_id == plugin_id
            )
            .count()
        )

    @staticmethod
    def cleanup_old_logs(
        db: Session,
        plugin_id: str,
        keep_last: int = 100,
    ) -> None:
        """
        Keep only the latest `keep_last` execution logs
        for a plugin and delete older logs.
        """

        logs = (
            db.query(ExecutionLog)
            .filter(
                ExecutionLog.plugin_id == plugin_id
            )
            .order_by(
                ExecutionLog.executed_at.desc()
            )
            .all()
        )

        if len(logs) <= keep_last:
            return

        old_logs = logs[keep_last:]

        for log in old_logs:
            db.delete(log)

        db.commit()