from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Skills(BaseModel):
    dept_id: UUID
    category_id: UUID
    name: str
    description: str
    author_id: UUID
    created_at: datetime = datetime.now().isoformat()
