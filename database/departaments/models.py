import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Departaments(Base):
    __tablename__ = "departaments"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    org_id = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    manager_id = Column(String, nullable=False)
    @staticmethod
    def serialize_departaments(departaments):
        serialize_departament = {}
        for departament in departaments:
            serialize_departament[str(departament.id)] = {
                "id": str(departament.id),
                "org_id": str(departament.org_id),
                "name": str(departament.name),
                "manager_id": str(departament.manager_id)
            }
        return serialize_departament