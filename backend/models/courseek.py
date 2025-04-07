from pydantic import BaseModel

from .academics.section import CatalogSection

class CourseSeekResponse(BaseModel):
    sections: list[CatalogSection] | None = None
    response: str