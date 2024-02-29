from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, time


#PROJECTS

class Projects(BaseModel):
    org_id: UUID
    name: str
    period: str
    start_date: datetime
    deadline_date: datetime
    status: str
    description: str
    tech_stack: list
    created_at: datetime = datetime.now().isoformat()

#PROJECTS MEMBERS

class Project_members(BaseModel):
    user_id: UUID
    proj_id: UUID

#PROJECT ASSIGNMENTS

class Project_assignments(BaseModel):
    proj_id: UUID
    user_id: UUID
    proj_manager_id: UUID
    proposal: bool
    deallocated: bool
    dealloc_reason: str
    work_hours: int
    comment: str

#USER TEAM ROLES

class User_team_roles(BaseModel):
    user_id: UUID
    role_id: UUID
    proposal: bool

#PROJECT TECH STACK SKILLS


class Project_tech_stack_skills(BaseModel):
    proj_id: UUID
    skill_id: UUID


#PROJECT NEEDED ROLES

class Project_needed_roles(BaseModel):
    proj_id: UUID
    role_id: UUID
    count: int