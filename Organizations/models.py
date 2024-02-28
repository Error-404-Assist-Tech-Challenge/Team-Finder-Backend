from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

#ORGANIZATIONS MODEL

class Organization(BaseModel):
    admin_id: UUID
    name: str
    hq_address: str
    created_at: datetime = datetime.now().isoformat()



#USER_ROLES MODEL
class UserRole(BaseModel):
    user_id: UUID
    role_id: UUID

#ORGANIZATION_ROLES MODEL
class Organization_roles(BaseModel):
    id: UUID
    name: str

#TEAM_ROLES
class Team_roles(BaseModel):
    id: UUID
    org_id: UUID
    name: str