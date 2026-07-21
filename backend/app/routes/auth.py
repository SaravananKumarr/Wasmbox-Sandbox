from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.auth import create_access_token, verify_password, get_password_hash, decode_access_token
from app.schemas.auth import UserCreate, UserLogin, Token
from app.models.user import User
from app.utils.response import success, error

router = APIRouter()


@router.post("/register", response_model=dict)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=get_password_hash(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return success("User registered")


@router.post("/login", response_model=dict)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return success("Login successful", {"access_token": access_token, "token_type": "bearer"})
