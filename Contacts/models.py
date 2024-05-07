from uuid import UUID
from typing import List
from pydantic import BaseModel


class Contact(BaseModel):
    id: UUID
    name: str
    email: str
    roles: List[str]