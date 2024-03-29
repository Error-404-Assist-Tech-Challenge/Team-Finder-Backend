from typing import Literal, Optional, List

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

# SKILL ENDORSEMENTS


class Endorsements(BaseModel):
    type: Optional[Literal['Course', 'Training', 'Project']]
    endorsement: str
    description: str
    proj_id: Optional[str]


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
    skill_id: Optional[str]
    level: int
    experience: int
    created_at: datetime = datetime.now().isoformat()
    # For skill endorsements
    endorsements: Optional[List[Endorsements]]


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
    endorsements: Optional[List[Endorsements]]


class RemoveSkill(BaseModel):
    skill_id: UUID


# SKILL_CATEGORIES

class SkillCategoriesResponse(BaseModel):
    label: str
    value: UUID
    is_used: bool = False


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


class AddDepartment(BaseModel):
    skill_id: UUID
    dept_id: UUID


class Remove_department_skill(BaseModel):
    skill_id: UUID

# SKILLS PROPOSALS


class Update_skill(BaseModel):
    user_id: UUID
    skill_id: Optional[str]
    proposal: bool


class Proposal(BaseModel):
    assignment_id: Optional[UUID]
    comment: Optional[str]
    dealloc_reason: Optional[str]
    deallocated: Optional[bool]
    experience: Optional[int]
    level: Optional[int]
    project_id: Optional[UUID]
    project_name: Optional[str]
    proposal: Optional[bool]
    role_ids: Optional[List[UUID]]
    role_names: Optional[List[str]]
    skill_id: Optional[UUID]
    skill_name: Optional[str]
    user_id: UUID
    user_name: str
    work_hours: Optional[int]


class EmployeeProposal(BaseModel):
    id: UUID
    name: str
    category_name: str
    description: str
    level: int
    experience: int


class AcceptEmployeeProposal(BaseModel):
    id: UUID
    level: int
    experience: int


class DeleteEmployeeProposal(BaseModel):
    id: UUID


# NOTIFICATIONS


class Notification(BaseModel):
    proposal_id: UUID
    skill_name: Optional[str]
    skill_id: Optional[UUID]
    proposal: bool
    project_name: Optional[str]
    deallocated: Optional[bool]
    dealloc_reason: Optional[str]
    user_name: Optional[str]
    for_employee: Optional[bool]
    level: Optional[str]
    experience: Optional[str]
    type: Optional[str]


class Put_Notifications(BaseModel):
    proposal_id: UUID



