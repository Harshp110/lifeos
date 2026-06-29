from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.tasks.schemas.tasks import TaskCreate, TaskUpdate


def create_task(db: Session, data: TaskCreate):
    user = db.query(User).first()

    if user is None:
        raise ValueError("No users found")

    task = Task(
        user_id=user.id,
        title=data.title,
        description=data.description,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(db: Session):
    return db.query(Task).all()


def get_task(db: Session, task_id: str):
    return db.get(Task, task_id)


def update_task(db: Session, task_id: str, data: TaskUpdate):
    task = db.get(Task, task_id)

    if task is None:
        return None

    if data.title is not None:
        task.title = data.title

    if data.description is not None:
        task.description = data.description

    if data.completed is not None:
        task.completed = data.completed

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: str):
    task = db.get(Task, task_id)

    if task is None:
        return False

    db.delete(task)
    db.commit()

    return True