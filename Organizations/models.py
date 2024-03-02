from pydantic import BaseModel
from typing import Literal, List
from uuid import UUID
from datetime import datetime

#ORGANIZATIONS

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


#USER_ROLES
class UserRole(BaseModel):
    user_id: UUID
    role_id: UUID


#ORGANIZATION_ROLES
class RoleData(BaseModel):
    id: UUID
    name: str


class RoleCreate(BaseModel):
    user_id: UUID
    role_name: Literal['admin', 'dept_manager', 'proj_manager']


class RoleResponse(BaseModel):
    user_id: UUID
    roles: List[str]


#TEAM_ROLES
class Team_roles(BaseModel):
    org_id: UUID
    name: str
