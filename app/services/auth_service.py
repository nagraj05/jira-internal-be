from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

def create_user(db: Session, name: str, email: str, password: str):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

def login_user(user: User):
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}