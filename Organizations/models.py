from pydantic import BaseModel
from typing import Literal, List
from uuid import UUID
from datetime import datetime


# ORGANIZATIONS
class Organization(BaseModel):
    name: str
    hq_address: str
    created_at: datetime = datetime.now().isoformat()


class OrganizationMember(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    roles: List[str]


# SKILLS
class Skill(BaseModel):
    id: UUID
    category_id: UUID
    author_id: UUID
    dept_id: List[UUID]
    dept_name: List[str]
    author_name: str
    category_name: str
    name: str
    description: str
    is_authored: bool
    is_department_managed: bool


class CreateSkill(BaseModel):
    category_id: UUID
    name: str
    description: str
    assign_department: bool


class DeleteSkill(BaseModel):
    id: UUID


class UpdateSkill(BaseModel):
    skill_id: UUID
    category_id: UUID
    name: str
    description: str


# USER_ROLES
class UserRole(BaseModel):
    user_id: UUID
    role_id: UUID


# ORGANIZATION_ROLES
class RoleData(BaseModel):
    id: UUID
    name: str


class RemoveRole(BaseModel):
    user_id: UUID
    role_name: Literal['admin', 'dept_manager', 'proj_manager']


class RoleCreate(BaseModel):
    user_id: UUID
    role_name: Literal['admin', 'dept_manager', 'proj_manager']


# TEAM_ROLES
class TeamRole(BaseModel):
    id: UUID
    name: str


class TeamRoleAll(BaseModel):
    value: UUID
    label: str


class TeamRoleCreate(BaseModel):
    name: str


class TeamRoleUpdate(BaseModel):
    id: UUID
    name: str


class TeamRoleDelete(BaseModel):
    id: UUID
