import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base

#SKILL_CATEGORIES

class Skill_categories(Base):
    __tablename__ = "skill_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    org_id = Column(UUID, ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    @staticmethod
    def serialize_skill_categories(skill_categories):
        serialize_skill_category = {}
        for skill_category in skill_categories:
            serialize_skill_category[str(skill_category.id)] = {
                "id": str(skill_category.id),
                "org_id": str(skill_category.org_id),
                "name": str(skill_category.name),
                "created_at": str(skill_category.created_at)
            }
        return serialize_skill_category


#SKILLS

class Skill(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    category_id = Column(UUID, ForeignKey("skill_categories.id"),nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    author_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    org_id = Column(UUID, ForeignKey("organizations.id"), nullable=False)

    @staticmethod
    def serialize_skills(skills):
        serialize_skills = {}
        for skill in skills:
            serialize_skills[str(skill.id)] = {
                "id": str(skill.id),
                "name": str(skill.name),
                "category_id": str(skill.category_id),
                "description": str(skill.description),
                "created_at": str(skill.created_at),
                "author_id": str(skill.author_id),
                "org_id": str(skill.org_id)
            }
        return serialize_skills

#USER_SKILLS
class UserSkills(Base):
    __tablename__ = "user_skills"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), primary_key=True, nullable=False)
    level = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    @staticmethod
    def serialize_user_skills(user_skills):
        serialized_user_skills = []
        for user_skill in user_skills:
            user_skill = {
                "user_id": str(user_skill.user_id),
                "skill_id": str(user_skill.skill_id),
                "level": str(user_skill.level),
                "experience": str(user_skill.experience),
                "created_at": str(user_skill.created_at)
            }
            serialized_user_skills.append(user_skill)
        return serialized_user_skills

#DEPARTMENT_SKILLS

class Department_skills(Base):
    __tablename__ = "department_skills"

    dept_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), primary_key=True, nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    @staticmethod
    def serialize_department_skills(department_skills):
        serialize_department_skills = {}
        for department_skill in department_skills:
            serialize_department_skills[str(department_skill.dept_id)] = {
                "dept_id": str(department_skill.dept_id),
                "skill_id": str(department_skill.skill_id)
            }
        return serialize_department_skills
