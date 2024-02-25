from pydantic import BaseModel
from uuid import UUID


class Departament(BaseModel):
    org_id: UUID
    name: str
    manager_id: UUID
