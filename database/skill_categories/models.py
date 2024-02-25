import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Skill_categories(Base):
    __tablename__ = "skill_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    dept_id = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    @staticmethod
    def serialize_skill_categories(skill_categories):
        serialize_skill_category = {}
        for skill_category in skill_categories:
            serialize_skill_category[str(skill_category.id)] = {
                "id": str(skill_category.id),
                "dept_id": str(skill_category.dept_id),
                "name": str(skill_category.name)
            }
        return serialize_skill_category
