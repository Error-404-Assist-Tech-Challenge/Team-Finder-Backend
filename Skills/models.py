from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# SKILLS MODELS

class Skills(BaseModel):
    dept_id: UUID
    category_id: UUID
    org_id: UUID
    name: str
    description: str
    author_id: UUID
    created_at: datetime = datetime.now().isoformat()


class SkillsResponse(BaseModel):
    user_id: UUID
    skill_id: UUID
    level: int
    experience: int
    created_at: str
    category_name: str
    skill_name: str
    skill_description: str
    skill_author: str

# USER_SKILLS MODELS


class UserSkills(BaseModel):
    skill_id: UUID
    level: int
    experience: int
    created_at: datetime = datetime.now().isoformat()


class SkillProposal(BaseModel):
    skill_id: UUID
    user_id: UUID
    level: int
    experience: int
    user_name: str
    type: str
    skill_name: str


class UpdateSkills(BaseModel):
    skill_id: UUID
    level: int
    experience: int


class RemoveSkill(BaseModel):
    skill_id: UUID


# SKILL_CATEGORIES

class SkillCategoriesResponse(BaseModel):
    label: str
    value: UUID


class SkillCategory(BaseModel):
    name: str
    created_at: datetime = datetime.now().isoformat()


class DeleteSkillCategory(BaseModel):
    id: UUID


class UpdateSkillCategory(BaseModel):
    id: UUID
    name: str
    modified_at: datetime = datetime.now().isoformat()

# DEPARTMENT_SKILLS


class Department_skills(BaseModel):
    skill_id: UUID
    dept_id: UUID


class AddDepartment(BaseModel):
    skill_id: UUID
    dept_id: UUID


class Remove_department_skill(BaseModel):
    skill_id: UUID

# SKILLS PROPOSALS


class Update_skill(BaseModel):
    user_id: UUID
    skill_id: UUID
    proposal: bool
