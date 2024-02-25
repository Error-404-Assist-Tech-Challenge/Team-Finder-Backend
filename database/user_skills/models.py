from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class UserSkills(Base):
    __tablename__ = "user_skills"

    user_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    skill_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)

    @staticmethod
    def serialize_user_skills(user_skills):
        serialized_user_skills = {}
        for user_skill in user_skills:
            serialized_user_skills[str(user_skill.user_id)] = {
                "user_id": str(user_skill.user_id),
                "skill_id": str(user_skill.skill_id)
            }
        return serialized_user_skills
