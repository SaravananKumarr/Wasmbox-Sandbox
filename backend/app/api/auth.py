from fastapi import APIRouter

from app.schemas.auth import LoginRequest
from app.schemas.auth import RegisterRequest

from app.services.auth_service import AuthService

router = APIRouter()

service = AuthService()


@router.post("/auth/register")
def register(user: RegisterRequest):

    return service.register(user)


@router.post("/auth/login")
def login(user: LoginRequest):

    token = service.login(user.email)

    return {
        "access_token": token,
        "token_type": "bearer"
    }