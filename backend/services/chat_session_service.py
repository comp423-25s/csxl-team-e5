import uuid
from sqlalchemy.orm import Session
from backend.entities.chat_session_entity import ChatSession


def create_session(db: Session, user_id: int) -> ChatSession:
    session = ChatSession(id=str(uuid.uuid4()), user_id=user_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def list_sessions(db: Session, user_id: int):
    return db.query(ChatSession).filter_by(user_id=user_id).all()


def get_session(db: Session, session_id: str, user_id: int):
    return db.query(ChatSession).filter_by(id=session_id, user_id=user_id).one_or_none()
