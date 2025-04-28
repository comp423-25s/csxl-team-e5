from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from backend.entities.chat_history import ChatHistory
from backend.models.semantic_chat_models import ChatHistoryResponse
from backend.services.chat_suggested_course_service import load_suggestions


def save_chat_message(
    db: Session,
    session_id: str,
    role: str,
    message: str,
) -> ChatHistoryResponse:
    chat_entry = ChatHistory(
        session_id=session_id,
        role=role,
        message=message,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)

    return ChatHistoryResponse(
        session_id=chat_entry.session_id,
        role=chat_entry.role,
        message=chat_entry.message,
        courses=[],
        timestamp=chat_entry.timestamp,
    )


def get_chat_history(
    db: Session,
    session_id: str,
) -> List[ChatHistoryResponse]:
    entries = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.timestamp.asc())
        .all()
    )

    history_responses: List[ChatHistoryResponse] = []
    for idx, entry in enumerate(entries):
        role: str = entry.role

        if role == "assistant":
            courses = load_suggestions(db, session_id, idx)
        else:
            courses = []

        history_responses.append(
            ChatHistoryResponse(
                session_id=entry.session_id,
                role=role,
                message=entry.message,
                courses=courses,
                timestamp=entry.timestamp,
            )
        )

    return history_responses
