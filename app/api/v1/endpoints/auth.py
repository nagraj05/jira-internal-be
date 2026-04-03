from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.auth import SignupRequest, TokenResponse
from app.services.auth_service import create_user, authenticate_user, login_user
from app.api.deps import get_db

router = APIRouter()

@router.post("/signup", response_model=TokenResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    user = create_user(db, data.name, data.email, data.password)
    return login_user(user)


@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form.username holds the email value
    user = authenticate_user(db, form.username, form.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return login_user(user)