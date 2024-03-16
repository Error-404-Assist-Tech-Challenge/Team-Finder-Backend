from typing import Optional, List

from pydantic import BaseModel,  validator, Field
from uuid import UUID
from datetime import datetime


# DEPARTMENT_MEMBERS
class Skill_endorsements(BaseModel):
    type: str
    endorsement: str
    description: str
    proj_id: Optional[str]


class DepartmentMember(BaseModel):
    user_id: UUID
    email: str
    name: str
    skills: Optional[List[str]] = Field(default_factory=list)
    endorsements: Optional[List[Skill_endorsements]] = Field(default_factory=list)


class CreateMember(BaseModel):
    user_id: UUID


class DeleteMember(BaseModel):
    user_id: UUID


# DEPARTMENTS
class DepartmentResponse(BaseModel):
    id: UUID
    org_id: UUID
    name: str
    manager_id: Optional[UUID]
    created_at: str
    department_members: List[DepartmentMember]
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


class RemoveDepartment(BaseModel):
    dept_id: UUID


class ManagedDepartment(BaseModel):
    name: str


class DepartmentProjectsResponse(BaseModel):
    proj_id: UUID
    project_name: str
    deadline_date: str
    status: str
    team_members: List[str]

