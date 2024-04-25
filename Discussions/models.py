from uuid import UUID
from pydantic import BaseModel


class Discussions(BaseModel):
    id: str = None
    contacts: list
    name: str = None
