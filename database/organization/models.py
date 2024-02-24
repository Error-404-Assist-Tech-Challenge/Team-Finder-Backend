import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Organization(Base):
    __tablename__ = "organization"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    admin_id = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    hq_address = Column(String, nullable=False)
    @staticmethod
    def serialize_organizations(organizations):
        serialize_organization = {}
        for organization in organizations:
            serialize_organization[str(organization.id)] = {
                "id": str(organization.id),
                "admin_id": str(organization.admin_id),
                "name": str(organization.name),
                "hq_address": str(organization.hq_address)
            }
        return serialize_organization