from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, nullable=False)
    role_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)

    @staticmethod
    def serialize_user_roles(user_roles):
        serialized_user_roles = {}
        for user_role in user_roles:
            serialized_user_roles[str(user_role.user_id)] = {
                "user_id": str(user_role.user_id),
                "role_id": str(user_role.role_id)
            }
        return serialized_user_roles
