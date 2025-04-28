# literally just a chat response (string) with nothing else

from pydantic import BaseModel

from backend.models.academics.course import Course
from backend.models.courseseek_course import CourseSeekCourse


class SimpleChatResponse(BaseModel):
    session_id: str
    message: str
    courses: list[CourseSeekCourse]
