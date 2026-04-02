from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.services.auth_service import create_user, authenticate_user, login_user
from app.api.deps import get_db

router = APIRouter()

@router.post("/signup", response_model=TokenResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    user = create_user(db, data.name, data.email, data.password)
    return login_user(user)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return login_user(user)