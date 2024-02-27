import uuid
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base

#DEPARTMENT_MEMBERS
class Department_members(Base):
    __tablename__ = "department_members"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    dept_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"),nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),nullable=False)
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

#DEPARTMENTS
class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"),nullable=False)
    name = Column(String, nullable=False)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),nullable=False)
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
