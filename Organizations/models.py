from pydantic import BaseModel
from typing import Literal
from uuid import UUID
from datetime import datetime

#ORGANIZATIONS MODEL

class Organization(BaseModel):
    name: str
    hq_address: str
    created_at: datetime = datetime.now().isoformat()



#USER_ROLES MODEL
class UserRole(BaseModel):
    user_id: UUID
    role_id: UUID

#ORGANIZATION_ROLES MODEL
class RoleData(BaseModel):
    id: UUID
    name: str

class RoleCreate(BaseModel):
    user_id: UUID
    role_name: Literal['admin', 'dept_manager', 'proj_manager']

#TEAM_ROLES
class Team_roles(BaseModel):
    org_id: UUID
    name: str
