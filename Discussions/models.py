from uuid import UUID
from typing import List
from pydantic import BaseModel


class Discussion(BaseModel):
    contacts: List[UUID]
    name: str = None


class ContactResponse(BaseModel):
    id: UUID
    name: str


class DiscussionsResponse(BaseModel):
    id: UUID
    contacts: List[ContactResponse]
    name: str