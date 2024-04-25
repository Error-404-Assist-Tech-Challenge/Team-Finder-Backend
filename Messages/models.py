from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Messages(BaseModel):
    discussion_id: str
    user_id: str
    value: str


class ResponseMessages(BaseModel):
    id: str
    discussion_id: str
    user_id: str
    value: str
    created_at: str


class Discussions(BaseModel):
    discussion_id: str