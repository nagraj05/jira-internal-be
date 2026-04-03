import os
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

def seed_admin():
    email = os.environ.get("ADMIN_EMAIL")
    password = os.environ.get("ADMIN_PASSWORD")

    if not email or not password:
        raise ValueError("ADMIN_EMAIL and ADMIN_PASSWORD environment variables must be set")

    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.is_admin == True).first()

        if existing_admin:
            print("✅ Admin already exists")
            return

        admin = User(
            name="Admin",
            email=email,
            hashed_password=hash_password(password),
            is_admin=True,
            is_active=True
        )

        db.add(admin)
        db.commit()

        print("🔥 Admin user created successfully")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()