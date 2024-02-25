from pydantic import BaseModel
from uuid import UUID


class Skill_categories(BaseModel):
    dept_id: UUID
    name: str
