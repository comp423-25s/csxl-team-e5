"""CoursSeek API

API for initiating chat with CourseSeek."""

from fastapi import APIRouter, FastAPI

from backend.models.academics.section import CatalogSection
from backend.models.courseek import CourseSeekResponse
from backend.models.public_user import PublicUser
from backend.models.room import Room

api = APIRouter(prefix = "api/academics/chat")

@api.post("", tags=["CourseSeek"])
def courseseek_chat(user_input: str) -> CourseSeekResponse:
    instructor = PublicUser(id=1, onyen=12345678, first_name="Brent", last_name="Munsell", pronouns="he/him", email="bmunsell@unc.edu")
    demo_section = CatalogSection(course_number="COMP 311", description="Brent Munsell typa stuff", enrolled=50, subject_code="COMP", section_number=1, lecture_room=Room(nickname="HM 100"), instructors=instructor, total_seats=150)
    return CourseSeekResponse(sections=demo_section, response="Test response")
