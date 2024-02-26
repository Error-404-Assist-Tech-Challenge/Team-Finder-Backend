from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Skill_categories(BaseModel):
    dept_id: UUID
    name: str
    created_at: datetime = datetime.now().isoformat()
