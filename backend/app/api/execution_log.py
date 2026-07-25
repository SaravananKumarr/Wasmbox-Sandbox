import csv
import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.dependencies.current_user import get_current_user
from app.schemas.execution_log import (
    ExecutionLogFilter,
    ExecutionLogListResponse,
    ExecutionLogResponse,
)
from app.services.execution_log_service import ExecutionLogService

router = APIRouter(
    prefix="/execution-logs",
    tags=["Execution Logs"],
)


@router.get(
    "/{plugin_id}",
    response_model=ExecutionLogListResponse,
)
def get_execution_logs(
    plugin_id: str,
    page: int = 1,
    limit: int = 10,
    status_filter: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        filters = ExecutionLogFilter(
            page=page,
            limit=limit,
            status=status_filter,
        )

        return ExecutionLogService.get_plugin_logs(
            db,
            plugin_id,
            filters,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get(
    "/log/{log_id}",
    response_model=ExecutionLogResponse,
)
def get_execution_log(
    log_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return ExecutionLogService.get_log(
            db,
            log_id,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{log_id}")
def delete_execution_log(
    log_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        ExecutionLogService.delete_log(
            db,
            log_id,
            current_user.id,
        )

        return {
            "message": "Execution log deleted successfully."
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get(
    "/export/{plugin_id}",
    response_model=list[ExecutionLogResponse],
)
def export_execution_logs(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return ExecutionLogService.export_logs(
            db,
            plugin_id,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/export/{plugin_id}/json")
def export_execution_logs_json(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return ExecutionLogService.export_logs(
            db,
            plugin_id,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/export/{plugin_id}/csv")
def export_execution_logs_csv(
    plugin_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        logs = ExecutionLogService.export_logs(
            db,
            plugin_id,
            current_user.id,
        )

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "Executed At",
            "Status",
            "Exit Code",
            "Duration (s)",
            "Memory Used (KB)",
            "Stdout",
            "Stderr",
        ])

        for log in logs:
            writer.writerow([
                log.executed_at,
                log.status,
                log.exit_code,
                log.duration,
                log.memory_used,
                log.stdout,
                log.stderr,
            ])

        output.seek(0)

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f'attachment; filename="{plugin_id}_execution_logs.csv"'
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))