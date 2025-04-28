from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .entity_base import EntityBase


class ChatHistory(EntityBase):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        String, ForeignKey("chat_session.id"), nullable=False, index=True
    )
    role = Column(String, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    session = relationship("ChatSession", back_populates="messages")
