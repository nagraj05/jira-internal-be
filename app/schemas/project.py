from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.models.enums import ProjectRole


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    pm_user_id: UUID


class AddMemberRequest(BaseModel):
    user_id: UUID
    role: ProjectRole


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    created_by: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectMemberResponse(BaseModel):
    id: UUID
    user_id: UUID
    project_id: UUID
    role: ProjectRole

    model_config = ConfigDict(from_attributes=True)
