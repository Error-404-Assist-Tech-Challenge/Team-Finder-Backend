from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


#SKILLS MODELS

class Skills(BaseModel):
    dept_id: UUID
    category_id: UUID
    org_id: UUID
    name: str
    description: str
    author_id: UUID
    created_at: datetime = datetime.now().isoformat()


#USER_SKILLS MODELS

class UserSkills(BaseModel):
    skill_id: UUID
    created_at: datetime = datetime.now().isoformat()

class UpdateSkills(BaseModel):
    user_id: str
    skill_id: str
    level: int
    experience: int

#SKILL_CATEGORIES

class Skill_categories(BaseModel):
    dept_id: UUID
    name: str
    created_at: datetime = datetime.now().isoformat()

class Update_skill_category(BaseModel):
    id: UUID
    org_id: UUID
    name: str
    modified_at: datetime = datetime.now().isoformat()

#DEPARTMENT_SKILLS

class Department_skills(BaseModel):
    skill_id: UUID
    dept_id: UUID
    new_dept_id: UUID
    new_skill_id: UUID
