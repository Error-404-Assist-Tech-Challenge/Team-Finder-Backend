import uuid
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    manager_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    @staticmethod
    def serialize_departments(departments):
        serialize_department = {}
        for department in departments:
            serialize_department[str(department.id)] = {
                "id": str(department.id),
                "org_id": str(department.org_id),
                "name": str(department.name),
                "manager_id": str(department.manager_id),
                "created_at": str(department.created_at)
            }
        return serialize_department
