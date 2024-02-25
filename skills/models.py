from pydantic import BaseModel
from uuid import UUID


class Skills(BaseModel):
    dept_id: UUID
    category_id: UUID
    name: str
    description: str
