from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service

router = APIRouter()


# ✅ CREATE TASK
@router.post("/{project_id}/tasks", response_model=TaskResponse)
def create_task(
    project_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task_service.assert_project_member(db, current_user.id, project_id)
    return task_service.create_task(db, project_id, current_user.id, data)


# ✅ GET ALL TASKS FOR A PROJECT
@router.get("/{project_id}/tasks", response_model=List[TaskResponse])
def get_project_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task_service.assert_project_member(db, current_user.id, project_id)
    return task_service.get_project_tasks(db, project_id)


# ✅ GET SINGLE TASK
@router.get("/{project_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task_service.assert_project_member(db, current_user.id, project_id)
    return task_service.get_task(db, task_id)


# ✅ UPDATE TASK
@router.patch("/{project_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    project_id: int,
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task_service.assert_project_member(db, current_user.id, project_id)
    return task_service.update_task(db, task_id, data)


# ✅ DELETE TASK
@router.delete("/{project_id}/tasks/{task_id}")
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task_service.assert_project_member(db, current_user.id, project_id)
    task_service.delete_task(db, task_id)
    return {"message": "Task deleted successfully"}
