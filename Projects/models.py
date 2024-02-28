from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

#PROJECTS

class Projects(BaseModel):
    id: UUID
    org_id: UUID
    name: str
    period: str
    start_date: datetime
    deadline_date: timestamp
    status: str
    description: str
    tech_stack: str
    created_at: timestamp