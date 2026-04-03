from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    is_admin = Column(Boolean, default=False)  # 🔥 IMPORTANT (only one admin)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    memberships = relationship("ProjectMember", back_populates="user")