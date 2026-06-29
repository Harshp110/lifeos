from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    content: str