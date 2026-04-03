from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

def seed_admin():
    db = SessionLocal()

    existing_admin = db.query(User).filter(User.is_admin == True).first()

    if existing_admin:
        print("✅ Admin already exists")
        return

    admin = User(
        name="Admin",
        email="otsiadmin@otsi.co.in",
        hashed_password=hash_password("Admin@123"),
        is_admin=True,
        is_active=True
    )

    db.add(admin)
    db.commit()

    print("🔥 Admin user created successfully")

    db.close()


if __name__ == "__main__":
    seed_admin()