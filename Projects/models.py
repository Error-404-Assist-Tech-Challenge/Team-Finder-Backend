from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, time, date
from typing import Literal, List


# PROJECTS

class Team_roles(BaseModel):
    role_id: UUID
    count: int


class DeleteProject(BaseModel):
    proj_id: UUID


class UpdateProject(BaseModel):
    proj_id: UUID
    name: str
    period: Literal['Fixed', 'Ongoing']
    start_date: date
    deadline_date: date
    status: Literal['Not started', 'Starting', 'In Progress', 'Closing', 'Closed']
    description: str
    created_at: datetime = datetime.now().isoformat()
    tech_stack: List[UUID]
    team_roles: List[Team_roles]


class Projects(BaseModel):
    name: str
    period: Literal['Fixed', 'Ongoing']
    start_date: date
    deadline_date: date
    status: Literal['Not Started', 'Starting', 'In Progress', 'Closing', 'Closed']
    description: str
    created_at: datetime = datetime.now().isoformat()
    tech_stack: List[UUID]
    team_roles: List[Team_roles]

# PROJECTS MEMBERS


class Project_members(BaseModel):
    user_id: UUID
    proj_id: UUID

# PROJECT ASSIGNMENTS


class Project_assignments(BaseModel):
    proj_id: UUID
    user_id: UUID
    proj_manager_id: UUID
    proposal: bool
    deallocated: bool
    dealloc_reason: str
    work_hours: int
    comment: str

# USER TEAM ROLES


class User_team_roles(BaseModel):
    user_id: UUID
    role_id: UUID
    proposal: bool



# PROJECT NEEDED ROLES

class Project_needed_roles(BaseModel):
    proj_id: UUID
    role_id: UUID
    count: int