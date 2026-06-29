from sqlalchemy.orm import Session

from app.habits.schemas.habits import HabitCreate, HabitUpdate
from app.models.habit import Habit
from app.models.user import User


def create_habit(db: Session, data: HabitCreate):
    user = db.query(User).first()

    habit = Habit(
        title=data.title,
        owner_id=user.id,
    )

    db.add(habit)
    db.commit()
    db.refresh(habit)

    return habit


def get_habits(db: Session):
    return db.query(Habit).all()


def get_habit(db: Session, habit_id: str):
    return db.get(Habit, habit_id)


def update_habit(db: Session, habit_id: str, data: HabitUpdate):
    habit = db.get(Habit, habit_id)

    if habit is None:
        return None

    if data.title is not None:
        habit.title = data.title

    if data.completed_today is not None:
        habit.completed_today = data.completed_today

    if data.streak is not None:
        habit.streak = data.streak

    db.commit()
    db.refresh(habit)

    return habit


def delete_habit(db: Session, habit_id: str):
    habit = db.get(Habit, habit_id)

    if habit is None:
        return False

    db.delete(habit)
    db.commit()

    return True
