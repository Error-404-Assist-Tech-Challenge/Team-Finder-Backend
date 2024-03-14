from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class Tech_stack(BaseModel):
    skill_id: UUID
    skill_name: str


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
    deadline_date: datetime
    status: str
    description: str
    can_be_deleted: bool
    tech_stack: List[Tech_stack]
    team_role: List[Team_roles]
    available_roles: List[Available_roles]


class Chat_Response(BaseModel):
    employees: List[str]


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
    current_work_hours: int
    work_hours: int


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
    past: Optional[List[UserResponse]]
    new: Optional[List[NewUserResponse]]

# Chat gpt request


class Chat_basemodel(BaseModel):
    context: str
    project_members: SearchResponse
    project: Project
