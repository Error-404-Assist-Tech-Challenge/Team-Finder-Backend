from typing import Optional

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# DEPARTMENTS
class Department(BaseModel):
    name: str
    created_at: datetime = datetime.now().isoformat()


class Modified_department(BaseModel):
    manager_id: Optional[str]
    dept_id: UUID
    name: str


# DEPARTMENT_MEMBERS
class Department_member(BaseModel):
    dept_id: UUID
    user_id: UUID
