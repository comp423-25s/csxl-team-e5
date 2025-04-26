from pydantic import BaseModel


class CourseSeekCourse(BaseModel):
    # matches the courses that courseseek will respond with
    course_number: str
    course_title: str
    credits: str
    description: str
    requirements: str
