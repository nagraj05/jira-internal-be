from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.models.enums import ProjectRole


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class AddMemberRequest(BaseModel):
    user_id: int
    role: ProjectRole


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectMemberResponse(BaseModel):
    id: int
    user_id: int
    project_id: int
    role: ProjectRole

    model_config = ConfigDict(from_attributes=True)
