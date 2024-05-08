from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Message(BaseModel):
    discussion_id: UUID
    value: str


class MessageResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    value: str
    created_at: str


class Discussions(BaseModel):
    discussion_id: str