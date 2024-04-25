import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Integer, DateTime
import datetime
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Messages(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    value = Column(String, nullable=False)
    discussion_id = Column(UUID(as_uuid=True), ForeignKey("discussions.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def serialize(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "value": str(self.value),
            "discussion_id": str(self.discussion_id),
            "created_at": str(self.created_at)
        }

    @staticmethod
    def serialize_messages(messages):
        messages_dict = {}
        for message in messages:
            messages_dict[str(message.id)] = {
                "id": str(message.id),
                "created_at": str(message.created_at),
                "discussion_id": str(message.discussion_id),
                "user_id": str(message.user_id),
                "value": str(message.value)
            }
        return messages_dict