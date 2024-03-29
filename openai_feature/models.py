from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class Team_roles(BaseModel):
    role_id: UUID
    count: int
    role_name: str


class Available_roles(BaseModel):
    value: UUID
    label: str


class Project(BaseModel):
    id: UUID
    name: str
    period: str
    start_date: datetime
    deadline_date: Optional[datetime]
    status: str
    description: str
    can_be_deleted: bool
    tech_stack: List[str]
    team_role: List[Team_roles]
    available_roles: List[Available_roles]


# Project Employees

class SkillResponse(BaseModel):
    name: str
    experience: int
    level: int


class RoleResponse(BaseModel):
    id: UUID
    name: str


class UserResponse(BaseModel):
    user_id: UUID
    name: str
    roles: List[RoleResponse]
    skills: List[SkillResponse]
    dept_name: str
    current_work_hours: Optional[int]
    work_hours: Optional[int]


class ActiveResponse(BaseModel):
    assignment_id: Optional[UUID]
    user_id: UUID
    name: str
    roles: List[RoleResponse]
    skills: List[SkillResponse]
    deallocate_comment: Optional[str]
    deallocate_proposal: Optional[bool]
    dept_name: str
    current_work_hours: Optional[int]
    work_hours: Optional[int]


class PastResponse(BaseModel):
    assignment_id: Optional[UUID]
    user_id: UUID
    name: str
    past_roles: List[RoleResponse]
    skills: List[SkillResponse]
    deallocate_comment: Optional[str]
    deallocate_proposal: Optional[bool]
    dept_name: str
    current_work_hours: Optional[int]
    work_hours: Optional[int]


class ProposedUserResponse(BaseModel):
    user_id: UUID
    name: str
    assignment_id: UUID
    proposed_roles: List[UUID]
    skills: List[SkillResponse]
    dept_name: str
    comment: str
    work_hours: int
    proposed_work_hours: int


class NewUserResponse(BaseModel):
    user_id: UUID
    name: str
    roles: List[RoleResponse]
    skills: List[SkillResponse]
    dept_name: str
    work_hours: int
    deadline: str


class SearchResponse(BaseModel):
    active: Optional[List[UserResponse]]
    proposed: Optional[List[ProposedUserResponse]]
    past: Optional[List[PastResponse]]
    new: Optional[List[NewUserResponse]]

# Chat gpt request


class Chat_basemodel(BaseModel):
    context: str
    project_members: SearchResponse
    project: Project


class Chat_Response(BaseModel):
    user_id: UUID
    deadline_date: Optional[datetime]
    name: str
    skills: List[SkillResponse]
    work_hours: Optional[int]