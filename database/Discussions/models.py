import uuid
from sqlalchemy import Column, String, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Discussions(Base):
    __tablename__ = "discussions"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    contacts = Column(ARRAY(UUID(as_uuid=True)), nullable=False)

    def serialize(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "contacts": str(self.contacts)
        }

    @staticmethod
    def serialize_discussions(discussions):
        discussions_dict = {}
        for discussion in discussions:
            serialized_contacts = [str(contact) for contact in discussion.contacts]
            discussions_dict[str(discussion.id)] = {
                "id": str(discussion.id),
                "contacts": serialized_contacts,
                "name": discussion.name
            }
        return discussions_dict

