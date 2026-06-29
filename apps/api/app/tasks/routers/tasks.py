from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.tasks.schemas.tasks import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.tasks.services.task_service import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    update_task,
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("", response_model=TaskResponse)
def create(
    data: TaskCreate,
    db: Annotated[Session, Depends(get_session)],
):
    return create_task(db, data)


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    db: Annotated[Session, Depends(get_session)],
):
    return get_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_one(
    task_id: UUID,
    db: Annotated[Session, Depends(get_session)],
):
    task = get_task(db, task_id)

    if task is None:
        raise HTTPException(404, "Task not found")

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update(
    task_id: UUID,
    data: TaskUpdate,
    db: Annotated[Session, Depends(get_session)],
):
    task = update_task(db, task_id, data)

    if task is None:
        raise HTTPException(404, "Task not found")

    return task


@router.delete("/{task_id}")
def delete(
    task_id: UUID,
    db: Annotated[Session, Depends(get_session)],
):
    deleted = delete_task(db, task_id)

    if not deleted:
        raise HTTPException(404, "Task not found")

    return {"message": "Task deleted successfully"}