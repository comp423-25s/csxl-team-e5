import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .entity_base import EntityBase


class ChatSession(EntityBase):
    __tablename__ = "chat_session"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    user = relationship("UserEntity", back_populates="chat_sessions")

    messages = relationship(
        "ChatHistory",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatHistory.timestamp",
    )
