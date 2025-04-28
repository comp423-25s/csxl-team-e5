from typing import List
from sqlalchemy.orm import Session

from backend.entities.chat_suggested_course_entity import ChatSuggestedCourseEntity
from backend.models.courseseek_course import CourseSeekCourse


def save_suggestions(
    db: Session,
    session_id: str,
    message_index: int,
    courses: List[CourseSeekCourse],
) -> None:
    (
        db.query(ChatSuggestedCourseEntity)
        .filter_by(session_id=session_id, message_index=message_index)
        .delete(synchronize_session=False)
    )

    for course in courses:
        entry = ChatSuggestedCourseEntity(
            session_id=session_id,
            message_index=message_index,
            course_number=course.course_number,
            course_title=course.course_title,
            credits=course.credits,
            description=course.description,
            requirements=course.requirements,
        )
        db.add(entry)

    db.commit()


def load_suggestions(
    db: Session,
    session_id: str,
    message_index: int,
) -> List[CourseSeekCourse]:
    rows = (
        db.query(ChatSuggestedCourseEntity)
        .filter_by(session_id=session_id, message_index=message_index)
        .order_by(ChatSuggestedCourseEntity.id.asc())
        .all()
    )

    return [
        CourseSeekCourse(
            course_number=row.course_number,
            course_title=row.course_title,
            credits=row.credits,
            description=row.description,
            requirements=row.requirements,
        )
        for row in rows
    ]
