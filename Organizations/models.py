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


class ModifiedSkill(BaseModel):
    skill_id: UUID
    category_id: UUID
    name: str
    description: str
    created_at: datetime = datetime.now().isoformat()


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


class RoleResponse(BaseModel):
    user_id: UUID
    roles: List[str]


# TEAM_ROLES
class TeamRole(BaseModel):
    name: str


class TeamRoleUpdate(BaseModel):
    id: UUID
    name: str

class TeamRoleDelete(BaseModel):
    id: UUID
