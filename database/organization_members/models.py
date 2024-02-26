import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Organization_members(Base):
    __tablename__ = "organization_members"

    org_id = Column(UUID, ForeignKey("organizations.id"), primary_key=True, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True, nullable=False)
    @staticmethod
    def serialize_organization_members(organization_members):
        serialize_organization_members = {}
        for organization_member in organization_members:
            serialize_organization_members[str(organization_member.user_id)] = {
                "org_id": str(organization_member.org_id),
                "user_id": str(organization_member.user_id)
            }
        return serialize_organization_members
