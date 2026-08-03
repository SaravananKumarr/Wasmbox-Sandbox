from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.execution_log import ExecutionLog
from app.models.plugin import Plugin
from app.sandbox.engine import execute_plugin
from app.sandbox.engine import get_active_sandbox_count
from app.utils.time import humanize_relative

DEFAULT_HISTORY_LIMIT = 50


def _serialize_log(log: ExecutionLog) -> dict:
    return {
        "id": log.id,
        "pluginName": log.plugin_name,
        "timestamp": humanize_relative(log.created_at),
        "duration": log.duration_ms,
        "memory": log.memory_mb,
        "status": log.status,
        "returnCode": log.return_code,
        "output": log.output,
        "logs": log.logs,
    }


def _update_plugin_stats(plugin: Plugin, duration_ms: float) -> None:
    plugin.executions += 1

    if plugin.avg_runtime_ms is None:
        plugin.avg_runtime_ms = duration_ms
    else:
        plugin.avg_runtime_ms = round(
            (plugin.avg_runtime_ms * (plugin.executions - 1) + duration_ms) / plugin.executions,
            2,
        )

    if plugin.status == "Draft":
        plugin.status = "Active"


def run_execution(
    db: Session,
    code: str,
    input_payload: str = "{}",
    plugin_id: Optional[str] = None,
) -> dict:
    plugin = db.get(Plugin, plugin_id) if plugin_id else None
    plugin_name = plugin.name if plugin else "draft"

    result = execute_plugin(code, input_payload)

    log = ExecutionLog(
        plugin_id=plugin.id if plugin else None,
        plugin_name=plugin_name,
        code=code,
        input_payload=input_payload,
        status=result["status"],
        return_code=result["return_code"],
        duration_ms=result["duration_ms"],
        memory_mb=result["memory_mb"],
        output=result["output"],
        logs=result["logs"],
        error_message=result["error_message"],
    )
    db.add(log)

    if plugin:
        _update_plugin_stats(plugin, result["duration_ms"])

    db.commit()
    db.refresh(log)

    return {
        "id": log.id,
        "status": log.status,
        "returnCode": log.return_code,
        "duration": log.duration_ms,
        "memory": log.memory_mb,
        "output": log.output,
        "logs": log.logs,
    }


def get_history(db: Session, limit: int = DEFAULT_HISTORY_LIMIT) -> list[dict]:
    logs = (
        db.query(ExecutionLog)
        .order_by(ExecutionLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_log(log) for log in logs]


def get_metrics_summary(db: Session) -> dict:
    total = db.query(func.count(ExecutionLog.id)).scalar() or 0

    if total == 0:
        return {
            "totalExecutions": 0,
            "successRate": "0%",
            "avgRuntimeMs": 0.0,
            "activeSandboxes": get_active_sandbox_count(),
            "peakMemoryMB": 0.0,
        }

    success_count = (
        db.query(func.count(ExecutionLog.id))
        .filter(ExecutionLog.status == "Success")
        .scalar()
        or 0
    )
    avg_runtime = db.query(func.avg(ExecutionLog.duration_ms)).scalar() or 0.0
    peak_memory = db.query(func.max(ExecutionLog.memory_mb)).scalar() or 0.0
    success_rate = round((success_count / total) * 100, 1)

    return {
        "totalExecutions": total,
        "successRate": f"{success_rate}%",
        "avgRuntimeMs": round(avg_runtime, 1),
        "activeSandboxes": get_active_sandbox_count(),
        "peakMemoryMB": round(peak_memory, 1),
    }
