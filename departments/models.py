from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Department(BaseModel):
    org_id: UUID
    name: str
    manager_id: UUID
    created_at: datetime = datetime.now().isoformat()
