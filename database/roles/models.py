from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), ForeignKey("user_roles.role_id"),primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    @staticmethod
    def serialize_roles(roles):
        serialized_roles = {}
        for role in roles:
            serialized_roles[str(role.id)] = {
                "name": role.name
            }
        return serialized_roles
