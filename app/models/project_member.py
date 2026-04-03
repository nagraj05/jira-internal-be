import uuid
from sqlalchemy import Column, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import ProjectRole


class ProjectMember(Base):
    __tablename__ = "project_members"

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_user_project"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)

    role = Column(Enum(ProjectRole), nullable=False)

    # relationships
    user = relationship("User", back_populates="memberships")
    project = relationship("Project", back_populates="members")