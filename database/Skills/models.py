import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Integer, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


# SKILL_CATEGORIES

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


# SKILLS

class Skill(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    category_id = Column(UUID, ForeignKey("skill_categories.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    author_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    org_id = Column(UUID, ForeignKey("organizations.id"), nullable=False)

    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "category_id": self.category_id,
            "description": self.description,
            "created_at": self.created_at,
            "author_id": self.author_id,
            "org_id": self.org_id
        }

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


# USER_SKILLS
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


# DEPARTMENT_SKILLS

class Department_skills(Base):
    __tablename__ = "department_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4())
    dept_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)

    @staticmethod
    def serialize_department_skills(department_skills):
        serialize_department_skills = {}
        for department_skill in department_skills:
            serialize_department_skills[str(department_skill.id)] = {
                "dept_id": str(department_skill.dept_id),
                "skill_id": str(department_skill.skill_id)
            }
        return serialize_department_skills


# SKILL PROPOSALS


class Skill_proposals(Base):
    __tablename__ = "skill_proposals"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    dept_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=True)
    level = Column(Integer, nullable=True)
    experience = Column(Integer, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    dealloc_reason = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    role_ids = Column(ARRAY(UUID), nullable=True)
    proposal = Column(Boolean, nullable=False)
    deallocated = Column(Boolean, nullable=True)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("project_assignments.id"), nullable=True)
    read = Column(Boolean, nullable=False)

    @staticmethod
    def serialize_skill_proposals(skill_proposals):
        serialized_skill = {}
        for skill_proposal in skill_proposals:
            if skill_proposal.skill_id is None:
                serialized_skill[str(skill_proposal.id)] = {
                    "id": str(skill_proposal.id),
                    "skill_id": None,
                    "assignment_id": str(skill_proposal.assignment_id),
                    "dept_id": str(skill_proposal.dept_id),
                    "role_ids": [str(role) for role in skill_proposal.role_ids],
                    "level": None,
                    "skill_name": None,
                    "experience": None,
                    "user_id": str(skill_proposal.user_id),
                    "dealloc_reason": str(skill_proposal.dealloc_reason),
                    "comment": str(skill_proposal.comment),
                    "proposal": str(skill_proposal.proposal),
                    "read": str(skill_proposal.read),
                    "deallocated": str(skill_proposal.deallocated),
                }
            else:
                serialized_skill[str(skill_proposal.id)] = {
                    "id": str(skill_proposal.id),
                    "skill_id": str(skill_proposal.skill_id),
                    "assignment_id": None,
                    "dept_id": str(skill_proposal.dept_id),
                    "role_ids": None,
                    "level": str(skill_proposal.level),
                    "experience": str(skill_proposal.experience),
                    "user_id": str(skill_proposal.user_id),
                    "dealloc_reason": None,
                    "comment": None,
                    "proposal": str(skill_proposal.proposal),
                    "read": str(skill_proposal.read),
                    "deallocated": None,
                }
        return serialized_skill


class Endorsements(Base):
    __tablename__ = "endorsements"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    endo = Column(String, nullable=False)
    description = Column(String, nullable=False)
    proj_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    type = Column(String, nullable=False)

    @staticmethod
    def serialize_endorsements(skill_endorsements):
        serialized_endorsements = []
        for endo in skill_endorsements:
            skill_endorsement = {
                "endorsement": str(endo.endo),
                "type": str(endo.type),
                "skill_id": str(endo.skill_id),
                "description": str(endo.description),
                "proj_id": str(endo.proj_id)
            }
            serialized_endorsements.append(skill_endorsement)
        return serialized_endorsements
