from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.habits.schemas.habits import HabitCreate, HabitResponse, HabitUpdate
from app.habits.services.habit_service import (
    create_habit,
    delete_habit,
    get_habit,
    get_habits,
    update_habit,
)

router = APIRouter(
    prefix="/habits",
    tags=["Habits"],
)


@router.post("", response_model=HabitResponse)
def create(
    data: HabitCreate,
    db: Annotated[Session, Depends(get_session)],
):
    return create_habit(db, data)


@router.get("", response_model=list[HabitResponse])
def list_all(
    db: Annotated[Session, Depends(get_session)],
):
    return get_habits(db)


@router.get("/{habit_id}", response_model=HabitResponse)
def get_one(
    habit_id: UUID,
    db: Annotated[Session, Depends(get_session)],
):
    habit = get_habit(db, habit_id)

    if habit is None:
        raise HTTPException(404, "Habit not found")

    return habit


@router.put("/{habit_id}", response_model=HabitResponse)
def update(
    habit_id: UUID,
    data: HabitUpdate,
    db: Annotated[Session, Depends(get_session)],
):
    habit = update_habit(db, habit_id, data)

    if habit is None:
        raise HTTPException(404, "Habit not found")

    return habit


@router.delete("/{habit_id}")
def delete(
    habit_id: UUID,
    db: Annotated[Session, Depends(get_session)],
):
    deleted = delete_habit(db, habit_id)

    if not deleted:
        raise HTTPException(404, "Habit not found")

    return {"message": "Habit deleted successfully"}
