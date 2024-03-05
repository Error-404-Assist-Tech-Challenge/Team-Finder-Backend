from typing import Optional

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# DEPARTMENTS
class Department(BaseModel):
    name: str
    created_at: datetime = datetime.now().isoformat()


class DepartmentUpdate(BaseModel):
    manager_id: Optional[UUID]
    dept_id: UUID
    name: str


# DEPARTMENT_MEMBERS
class DepartmentMember(BaseModel):
    dept_id: UUID
    user_id: UUID
