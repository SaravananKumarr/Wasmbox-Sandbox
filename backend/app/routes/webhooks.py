from fastapi import APIRouter, Request, HTTPException
from app.utils.response import success, error

router = APIRouter()


@router.post("/webhook/test", response_model=dict)
def webhook_test(request: Request):
    payload = request.json()
    return success("Webhook received", {"received": payload})
