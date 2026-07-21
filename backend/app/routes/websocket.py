from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.response import success, error

router = APIRouter()

@router.websocket("/ws/execution/{execution_id}")
async def websocket_execution(websocket: WebSocket, execution_id: str):
    await websocket.accept()
    try:
        await websocket.send_text(f"Connected to execution stream: {execution_id}")
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        await websocket.close()
