from pydantic import BaseModel
from uuid import UUID


class Organization_member(BaseModel):
    org_id: UUID
    user_id: UUID
