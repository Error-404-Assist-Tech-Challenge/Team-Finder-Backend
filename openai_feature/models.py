from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class Skills(BaseModel):
    name: str
    experience: int
    level: int


class Roles(BaseModel):
    id: UUID
    name: str


class Active_members(BaseModel):
    user_id: UUID
    name: str
    roles: List[Roles]
    skills: List[Skills]
    dept_name: str
    current_work_hours: 1
    work_hours: int


class New(BaseModel):
    user_id: UUID
    name: str
    roles: Optional[List[Roles]]
    skills: List[Skills]
    dept_name: str
    current_work_hours: 1
    work_hours: int


class Project_Members(BaseModel):
    active: Optional[List[Active_members]]
    new: Optional[List[str]]
    past: Optional[List[str]]
    proposed: Optional[List[str]]


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


class Chat_basemodel(BaseModel):
    context: str
    project_members: Project_Members
    project: Project


class Chat_Response(BaseModel):
    employees: List[str]