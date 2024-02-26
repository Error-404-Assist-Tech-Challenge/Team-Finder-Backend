from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Organization(BaseModel):
    admin_id: UUID
    name: str
    hq_address: str
    created_at: datetime = datetime.now().isoformat()
