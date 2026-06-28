from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    completed: bool