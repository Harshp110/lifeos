from uuid import UUID

from pydantic import BaseModel, ConfigDict


class HabitCreate(BaseModel):
    title: str


class HabitUpdate(BaseModel):
    title: str | None = None
    completed_today: bool | None = None
    streak: int | None = None


class HabitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    streak: int
    completed_today: bool
