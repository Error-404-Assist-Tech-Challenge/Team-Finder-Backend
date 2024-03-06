from typing import Optional, List

from pydantic import BaseModel,  validator
from uuid import UUID
from datetime import datetime


# DEPARTMENT_MEMBERS
class DepartmentMember(BaseModel):
    user_id: UUID


class Delete_member(BaseModel):
    user_id: UUID


class DepartmentMemberResponse(BaseModel):
    user_id: UUID
    dept_id: UUID
    user_name: str


# DEPARTMENTS
class DepartmentResponse(BaseModel):
    id: UUID
    org_id: UUID
    name: str
    manager_id: Optional[UUID]
    created_at: str
    department_members: List[DepartmentMemberResponse]
    manager_name: str

    @validator('manager_id', pre=True)
    def validate_manager_id(cls, value):
        if isinstance(value, str) and value.lower() == 'none':
            return None
        return value

class Department(BaseModel):
    name: str
    created_at: datetime = datetime.now().isoformat()


class DepartmentUpdate(BaseModel):
    manager_id: Optional[UUID]
    dept_id: UUID
    name: str


class Remove_department(BaseModel):
    dept_id: UUID
