from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:

    def register(
        self,
        db: Session,
        user: RegisterRequest,
    ):

        # Check username
        existing_username = user_repository.get_by_username(
            db=db,
            username=user.username,
        )

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        # Check email
        existing_email = user_repository.get_by_email(
            db=db,
            email=user.email,
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

        # Create new user
        new_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
        )

        return user_repository.create(
            db=db,
            user=new_user,
        )

    def login(
        self,
        db: Session,
        user: LoginRequest,
    ):

        db_user = user_repository.get_by_email(
            db=db,
            email=user.email,
        )

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            user.password,
            db_user.password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token = create_access_token(
            {
                "sub": db_user.email,
                "user_id": db_user.id,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }


auth_service = AuthService()