from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.tasks.schemas.tasks import TaskCreate


def create_task(
    db: Session,
    data: TaskCreate,
):
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


def get_tasks(
    db: Session,
):
    return db.query(Task).all()