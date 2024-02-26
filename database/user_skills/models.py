from sqlalchemy import Column, Integer, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class UserSkills(Base):
    __tablename__ = "user_skills"

    user_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    skill_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    level = Column(Integer,nullable=False)
    experience = Column(Integer,nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    @staticmethod
    def serialize_user_skills(user_skills):
        serialized_user_skills = {}
        for user_skill in user_skills:
            serialized_user_skills[str(user_skill.user_id)] = {
                "user_id": str(user_skill.user_id),
                "skill_id": str(user_skill.skill_id),
                "level": str(user_skill.level),
                "experience": str(user_skill.experience),
                "created_at": str(user_skill.created_at)
            }
        return serialized_user_skills
