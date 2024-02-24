import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    @staticmethod
    def serialize_employees(employees):
        serialized_employees = {}
        for employee in employees:
            serialized_employees[str(employee.id)] = {
                "id": str(employee.id),
                "name": str(employee.name),
                "email": str(employee.email),
                "password": str(employee.password)
            }
        return serialized_employees

class Admin(Base):
    __tablename__ = "admin"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    oname = Column(String, nullable=False)
    address = Column(String, nullable=False)
    @staticmethod
    def serialize_admin(admins):
        serialize_admin = {}
        for admin in admins:
            serialize_admin[str(admin.id)] = {
                "id": str(admin.id),
                "name": str(admin.name),
                "email": str(admin.email),
                "password": str(admin.password),
                "oname": str(admin.oname),
                "address": str(admin.address)
            }
        return serialize_admin
