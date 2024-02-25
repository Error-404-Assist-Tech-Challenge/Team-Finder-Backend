from pydantic import BaseModel
from uuid import UUID


class UserSkills(BaseModel):
    user_id: UUID
    skill_id: UUID
    level: int
    exprience: int
