from sqlalchemy import Column, Integer, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import ProjectRole


class ProjectMember(Base):
    __tablename__ = "project_members"

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_user_project"),
    )

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    role = Column(Enum(ProjectRole), nullable=False)

    # relationships
    user = relationship("User", back_populates="memberships")
    project = relationship("Project", back_populates="members")