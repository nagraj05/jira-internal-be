from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.task import Task
from app.models.project_member import ProjectMember
from app.schemas.task import TaskCreate, TaskUpdate


def assert_project_member(db: Session, user_id: int, project_id: int):
    membership = db.query(ProjectMember).filter_by(
        user_id=user_id, project_id=project_id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this project")


def create_task(db: Session, project_id: int, reporter_id: int, data: TaskCreate) -> Task:
    if data.assignee_id:
        assignee_member = db.query(ProjectMember).filter_by(
            user_id=data.assignee_id, project_id=project_id
        ).first()
        if not assignee_member:
            raise HTTPException(status_code=400, detail="Assignee is not a member of this project")

    task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
        task_type=data.task_type,
        project_id=project_id,
        reporter_id=reporter_id,
        assignee_id=data.assignee_id,
        due_date=data.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def get_project_tasks(db: Session, project_id: int) -> list[Task]:
    return db.query(Task).filter(Task.project_id == project_id).all()


def update_task(db: Session, task_id: int, data: TaskUpdate) -> Task:
    task = get_task(db, task_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> None:
    task = get_task(db, task_id)
    db.delete(task)
    db.commit()
