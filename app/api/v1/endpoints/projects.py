from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.enums import ProjectRole
from app.models.user import User
from app.schemas.project import ProjectCreate, AddMemberRequest, ProjectResponse, ProjectMemberResponse

router = APIRouter()


# ✅ CREATE PROJECT
@router.post("/", response_model=ProjectResponse)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # create project
    project = Project(
        name=data.name,
        description=data.description,
        created_by=current_user.id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    # add creator as PM
    member = ProjectMember(
        user_id=current_user.id,
        project_id=project.id,
        role=ProjectRole.PM
    )

    db.add(member)
    db.commit()

    return project


# ✅ ADD MEMBER (PM ONLY)
@router.post("/{project_id}/members")
def add_member(
    project_id: int,
    data: AddMemberRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # check project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # check current user is PM
    membership = db.query(ProjectMember).filter_by(
        user_id=current_user.id,
        project_id=project_id
    ).first()

    if not membership or membership.role != ProjectRole.PM:
        raise HTTPException(status_code=403, detail="Only PM can add members")

    # check user exists
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # prevent duplicate members
    existing = db.query(ProjectMember).filter_by(
        user_id=data.user_id,
        project_id=project_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already in project")

    # add member
    new_member = ProjectMember(
        user_id=data.user_id,
        project_id=project_id,
        role=data.role
    )

    db.add(new_member)
    db.commit()

    return {"message": "User added successfully"}


# ✅ GET PROJECTS FOR CURRENT USER
@router.get("/", response_model=List[ProjectResponse])
def get_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projects = (
        db.query(Project)
        .join(ProjectMember, ProjectMember.project_id == Project.id)
        .filter(ProjectMember.user_id == current_user.id)
        .all()
    )

    return projects


# ✅ GET PROJECT MEMBERS
@router.get("/{project_id}/members", response_model=List[ProjectMemberResponse])
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # check membership
    membership = db.query(ProjectMember).filter_by(
        user_id=current_user.id,
        project_id=project_id
    ).first()

    if not membership:
        raise HTTPException(status_code=403, detail="Not part of this project")

    members = db.query(ProjectMember).filter_by(
        project_id=project_id
    ).all()

    return members
