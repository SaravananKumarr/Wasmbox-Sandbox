from sqlalchemy.orm import Session

from app.models.execution_log import ExecutionLog
from app.repositories.execution_log_repository import (
    ExecutionLogRepository,
)
from app.repositories.plugin_repository import PluginRepository
from app.schemas.execution_log import (
    ExecutionLogFilter,
    ExecutionLogListResponse,
)


class ExecutionLogService:

    @staticmethod
    def create_log(
        db: Session,
        plugin_id: str,
        status: str,
        stdout: str | None,
        stderr: str | None,
        exit_code: int,
        duration: float,
        memory_used: int | None = None,
    ) -> ExecutionLog:

        plugin = PluginRepository.get_by_id(
            db,
            plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        log = ExecutionLog(
            plugin_id=plugin_id,
            status=status,
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            duration=duration,
            memory_used=memory_used,
        )

        # Save execution log
        created = ExecutionLogRepository.create(
            db,
            log,
        )

        # Keep only the latest 100 logs
        ExecutionLogRepository.cleanup_old_logs(
            db,
            plugin_id,
            keep_last=100,
        )

        return created

    @staticmethod
    def get_plugin_logs(
        db: Session,
        plugin_id: str,
        filters: ExecutionLogFilter,
        current_user_id: str,
    ) -> ExecutionLogListResponse:

        plugin = PluginRepository.get_by_id(
            db,
            plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "You are not allowed to view these logs."
            )

        total, logs = ExecutionLogRepository.get_plugin_logs(
            db,
            plugin_id,
            filters,
        )

        return ExecutionLogListResponse(
            total=total,
            page=filters.page,
            limit=filters.limit,
            items=logs,
        )

    @staticmethod
    def get_log(
        db: Session,
        log_id: str,
        current_user_id: str,
    ) -> ExecutionLog:

        log = ExecutionLogRepository.get_by_id(
            db,
            log_id,
        )

        if not log:
            raise ValueError("Execution log not found.")

        plugin = PluginRepository.get_by_id(
            db,
            log.plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "You are not allowed to view this log."
            )

        return log

    @staticmethod
    def delete_log(
        db: Session,
        log_id: str,
        current_user_id: str,
    ) -> None:

        log = ExecutionLogRepository.get_by_id(
            db,
            log_id,
        )

        if not log:
            raise ValueError("Execution log not found.")

        plugin = PluginRepository.get_by_id(
            db,
            log.plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "You are not allowed to delete this log."
            )

        ExecutionLogRepository.delete(
            db,
            log,
        )

    @staticmethod
    def export_logs(
        db: Session,
        plugin_id: str,
        current_user_id: str,
    ) -> list[ExecutionLog]:

        plugin = PluginRepository.get_by_id(
            db,
            plugin_id,
        )

        if not plugin:
            raise ValueError("Plugin not found.")

        if plugin.user_id != current_user_id:
            raise PermissionError(
                "You are not allowed to export these logs."
            )

        return ExecutionLogRepository.get_plugin_all_logs(
            db,
            plugin_id,
        )