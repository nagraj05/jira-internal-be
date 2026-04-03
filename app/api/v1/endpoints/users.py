from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.core.security import hash_password
from app.schemas.auth import UserCreate
from app.schemas.user import UserResponse

router = APIRouter()


# ✅ GET CURRENT USER (must be defined before any /{id} routes)
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# ✅ GET ALL USERS (used for dropdowns like assign PM)
@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # only admin can see all users
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    users = db.query(User).all()

    return users


# ✅ CREATE USER (admin creates user)
@router.post("/", response_model=UserResponse)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # only admin can create users
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can create users")

    # check if user exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        is_active=True,
        is_admin=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user