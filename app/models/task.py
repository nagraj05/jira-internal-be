import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
from app.models.enums import TaskStatus, TaskPriority, TaskType


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    title = Column(String, nullable=False)

    description = Column(String, nullable=True)

    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)

    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)

    task_type = Column(Enum(TaskType), nullable=False, default=TaskType.TASK)

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)

    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    due_date = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", foreign_keys=[assignee_id])
    reporter = relationship("User", foreign_keys=[reporter_id])
