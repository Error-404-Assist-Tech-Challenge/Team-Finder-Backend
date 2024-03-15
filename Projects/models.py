from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, time, date
from typing import Literal, List, Optional


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
    start_date: datetime
    deadline_date: Optional[datetime]
    status: Literal['Not Started', 'Starting', 'In Progress', 'Closing', 'Closed']
    description: str
    created_at: datetime = datetime.now().isoformat()
    required_skills: List[UUID]
    tech_stack: List[str]
    team_roles: List[Team_roles]


class Projects(BaseModel):
    name: str
    period: Literal['Fixed', 'Ongoing']
    start_date: datetime
    deadline_date: Optional[datetime]
    status: Literal['Not Started', 'Starting', 'In Progress', 'Closing', 'Closed']
    description: str
    created_at: datetime = datetime.now().isoformat()
    required_skills: List[UUID]
    tech_stack: List[str]
    team_roles: List[Team_roles]

# PROJECTS MEMBERS


class Project_members(BaseModel):
    user_id: UUID
    proj_id: UUID


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
    assignment_id: UUID
    deallocate_proposal: bool = False
    deallocate_comment: str = ""
    roles: List[RoleResponse]
    skills: List[SkillResponse]
    dept_name: str
    current_work_hours: int
    work_hours: int


class PastUserResponse(BaseModel):
    user_id: UUID
    name: str
    assignment_id: UUID
    deallocate_proposal: bool = False
    deallocate_comment: str = ""
    past_roles: List[RoleResponse]
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
    past: Optional[List[PastUserResponse]]
    new: Optional[List[NewUserResponse]]


# PROJECT ASSIGNMENTS

class AssignmentProposal(BaseModel):
    user_id: UUID
    role_ids: List[UUID]
    proj_id: UUID
    work_hours: int
    comment: str


class DeallocationProposal(BaseModel):
    assignment_id: UUID
    user_id: UUID
    proj_id: UUID
    comment: str


class DeleteDeallocationProposal(BaseModel):
    assignment_id: UUID
    proj_id: UUID


class UpdateDeallocationProposal(BaseModel):
    assignment_id: UUID
    proj_id: UUID
    comment: str


class UpdateAssignmentProposal(BaseModel):
    assignment_id: UUID
    role_ids: List[UUID]
    proj_id: UUID
    proposed_work_hours: int
    comment: str


class DeleteAssignmentProposal(BaseModel):
    assignment_id: UUID
    proj_id: UUID


class ManageProposal(BaseModel):
    assignment_id: UUID
    action: Literal['Accept', 'Reject']
    type: Literal['Assignment', 'Deallocation']


# USER TEAM ROLES


class User_team_roles(BaseModel):
    user_id: UUID
    role_id: UUID
    proposal: bool


# PROJECT NEEDED ROLES

class ProjectNeededRoles(BaseModel):
    proj_id: UUID
    role_id: UUID
    count: int


class UpdateProjectNeededRoles(BaseModel):
    id: UUID
    count: int
