from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.tasks.schemas.tasks import (
    TaskCreate,
    TaskResponse,
)
from app.tasks.services.task_service import (
    create_task,
    get_tasks,
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