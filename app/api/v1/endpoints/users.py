from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.core.security import hash_password

router = APIRouter()


# ✅ GET ALL USERS (used for dropdowns like assign PM)
@router.get("/")
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
@router.post("/")
def create_user(
    name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # only admin can create users
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can create users")

    # check if user exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        is_active=True,
        is_admin=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ✅ GET CURRENT USER
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user