from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.user import User
from app.notes.schemas.notes import NoteCreate, NoteUpdate


def create_note(db: Session, data: NoteCreate):
    user = db.query(User).first()

    note = Note(
        owner_id=user.id,
        title=data.title,
        content=data.content,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


def get_notes(db: Session):
    return db.query(Note).all()


def get_note(db: Session, note_id: str):
    return db.get(Note, note_id)


def update_note(db: Session, note_id: str, data: NoteUpdate):
    note = db.get(Note, note_id)

    if note is None:
        return None

    if data.title is not None:
        note.title = data.title

    if data.content is not None:
        note.content = data.content

    db.commit()
    db.refresh(note)

    return note


def delete_note(db: Session, note_id: str):
    note = db.get(Note, note_id)

    if note is None:
        return False

    db.delete(note)
    db.commit()

    return True