from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import auth_service


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/auth/register")
def register(
    user: RegisterRequest,
    db: Session = Depends(get_db),
):
    return auth_service.register(
        db=db,
        user=user,
    )


@router.post("/auth/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db),
):
    return auth_service.login(
        db=db,
        user=user,
    )