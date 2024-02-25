import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Department_members(Base):
    __tablename__ = "department_members"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    dept_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    @staticmethod
    def serialize_department_members(members):
        serialize_department_members = {}
        for member in members:
            serialize_department_members[str(member.id)] = {
                "id": str(member.id),
                "dept_id": str(member.dept_id),
                "user_id": str(member.user_id)
            }
        return serialize_department_members
