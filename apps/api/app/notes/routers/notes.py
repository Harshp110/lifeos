from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.notes.schemas.notes import (
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)
from app.notes.services.note_service import (
    create_note,
    delete_note,
    get_note,
    get_notes,
    update_note,
)

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post("", response_model=NoteResponse)
def create(
    data: NoteCreate,
    db: Annotated[Session, Depends(get_session)],
):
    return create_note(db, data)


@router.get("", response_model=list[NoteResponse])
def list_notes(
    db: Annotated[Session, Depends(get_session)],
):
    return get_notes(db)


@router.get("/{note_id}", response_model=NoteResponse)
def get_one(
    note_id: UUID,
    db: Annotated[Session, Depends(get_session)],
):
    note = get_note(db, note_id)

    if note is None:
        raise HTTPException(404, "Note not found")

    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update(
    note_id: UUID,
    data: NoteUpdate,
    db: Annotated[Session, Depends(get_session)],
):
    note = update_note(db, note_id, data)

    if note is None:
        raise HTTPException(404, "Note not found")

    return note


@router.delete("/{note_id}")
def delete(
    note_id: UUID,
    db: Annotated[Session, Depends(get_session)],
):
    deleted = delete_note(db, note_id)

    if not deleted:
        raise HTTPException(404, "Note not found")

    return {"message": "Note deleted successfully"}