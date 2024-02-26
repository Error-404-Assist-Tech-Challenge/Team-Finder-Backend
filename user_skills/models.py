from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserSkills(BaseModel):
    user_id: UUID
    skill_id: UUID
    level: int
    experience: int
    created_at: datetime = datetime.now().isoformat()
