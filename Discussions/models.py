from uuid import UUID
from typing import List
from pydantic import BaseModel


class Discussion(BaseModel):
    contacts: List[UUID]
    name: str = None
