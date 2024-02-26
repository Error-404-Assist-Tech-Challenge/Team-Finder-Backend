from pydantic import BaseModel
from uuid import UUID

class UserRole(BaseModel):
    user_id: UUID
    role_id: UUID
