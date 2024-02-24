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
