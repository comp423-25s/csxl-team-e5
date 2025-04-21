# literally just a chat response (string) with nothing else

from pydantic import BaseModel

from backend.models.academics.course import Course


class SimpleChatResponse(BaseModel):
    message: str
    courses: list[Course]
