from pydantic import BaseModel
from uuid import UUID


class Department_member(BaseModel):
    dept_id: UUID
    user_id: UUID
