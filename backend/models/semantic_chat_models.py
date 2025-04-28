from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from backend.models.courseseek_course import CourseSeekCourse


class ChatRequest(BaseModel):
    session_id: str = ""
    input: str


class ChatHistoryResponse(BaseModel):
    session_id: str
    role: str
    message: str
    courses: List[CourseSeekCourse] = Field(default_factory=list)
    timestamp: datetime


class SessionResourceResponse(BaseModel):
    session_id: str
    latest_message: ChatHistoryResponse
