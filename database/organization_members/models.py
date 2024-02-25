import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Organization_members(Base):
    __tablename__ = "organization_members"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    org_id = Column(UUID, nullable=False)
    user_id = Column(UUID, nullable=False)
    @staticmethod
    def serialize_organization_members(organization_members):
        serialize_organization_members = {}
        for organization_member in organization_members:
            serialize_organization_members[str(organization_member.id)] = {
                "id": str(organization_member.id),
                "org_id": str(organization_member.org_id),
                "user_id": str(organization_member.user_id)
            }
        return serialize_organization_members
