from pydantic import BaseModel
from uuid import UUID


class Organization(BaseModel):
    admin_id: UUID
    name: str
    hq_address: str
