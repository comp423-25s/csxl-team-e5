"""CoursSeek API

API for initiating chat with CourseSeek."""

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from backend.models.academics.section import CatalogSection
from backend.models.courseek import CourseSeekResponse
from backend.models.public_user import PublicUser
from backend.models.room import Room

api = APIRouter(prefix = "/api/academics/chat")

class CourseSeekRequest(BaseModel):
    input: str

@api.post("", tags=["CourseSeek"])
def courseseek_chat(payload: CourseSeekRequest) -> CourseSeekResponse:
    instructor = PublicUser(
        id=1,
        onyen="12345678",
        first_name="Brent",
        last_name="Munsell",
        pronouns="he/him",
        email="bmunsell@unc.edu"
    )
    demo_section = CatalogSection(
        course_number="COMP 311",
        description="Brent Munsell typa stuff",
        enrolled=50,
        subject_code="COMP",
        section_number="1",
        title="BRENT",
        meeting_pattern="MWF",
        lecture_room=Room(id="1", nickname="HM 100"),
        instructors=[instructor],
        total_seats=150
    )
    return CourseSeekResponse(sections=[demo_section], response=f"Echo: {payload.input}")