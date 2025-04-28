from sqlalchemy import Column, Integer, String, ForeignKey
from backend.entities.entity_base import EntityBase


class ChatSuggestedCourseEntity(EntityBase):

    __tablename__ = "chat_suggested_courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(
        String,
        ForeignKey("chat_session.id", ondelete="CASCADE"),
        nullable=False,
    )
    message_index = Column(Integer, nullable=False)
    course_number = Column(String, nullable=False)
    course_title = Column(String, nullable=False)
    credits = Column(String, nullable=True)
    description = Column(String, nullable=True)
    requirements = Column(String, nullable=True)
