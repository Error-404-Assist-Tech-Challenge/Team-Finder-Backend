import uuid
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Skills(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    dept_id = Column(UUID, nullable=False)
    category_id = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    @staticmethod
    def serialize_skills(skills):
        serialize_skills = {}
        for skill in skills:
            serialize_skills[str(skill.id)] = {
                "id": str(skill.id),
                "dept_id": str(skill.dept_id),
                "name": str(skill.name),
                "category_id": str(skill.category_id),
                "description": str(skill.description),
                "created_at": str(skill.created_at)
            }
        return serialize_skills
