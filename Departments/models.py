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


class Remove_department(BaseModel):
    dept_id: UUID


class Delete_member(BaseModel):
    user_id: UUID


# DEPARTMENT_MEMBERS
class DepartmentMember(BaseModel):
    user_id: UUID
