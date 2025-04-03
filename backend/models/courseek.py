from pydantic import BaseModel

from .academics.section import CatalogSection

class CourseSeekResponse(BaseModel):
    id: int
    sections: list[CatalogSection] | None = None
    response: str