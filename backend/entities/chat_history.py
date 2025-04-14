from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .entity_base import EntityBase


class ChatHistory(EntityBase):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    role = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(
        DateTime, default=lambda: datetime.now(datetime.timezone.utc), nullable=False
    )
