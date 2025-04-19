from sqlalchemy.orm import Session
from backend.entities.chat_history import ChatHistory
from datetime import datetime, timezone


def save_chat_message(db: Session, session_id: str, role: str, message: str):
    chat_entry = ChatHistory(
        session_id=session_id,
        role=role,
        message=message,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)
    return chat_entry


def get_chat_history(db: Session, session_id: str):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.timestamp.asc())
        .all()
    )
