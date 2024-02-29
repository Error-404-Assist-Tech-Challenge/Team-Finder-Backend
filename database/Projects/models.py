import uuid
from sqlalchemy import Column, String, DateTime, TIMESTAMP, ForeignKey, INTEGER, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from database.db import Base

#PROJECTS
class Projects(Base):
    __tablename__ = "projects"

    id = Column(UUID, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    org_id = Column(UUID, ForeignKey("organizations.id"), nullable=False)
    period = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    deadline_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tech_stack = Column(ARRAY(String), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    @staticmethod
    def serialize_projects(projects):
        serialized_projects = {}
        for project in projects:
            serialized_projects[str(project.id)] = {
                "id": str(project.id),
                "name": str(project.name),
                "org_id": str(project.org_id),
                "period": str(project.period),
                "start_date": str(project.start_date),
                "deadline_date": str(project.deadline_date),
                "status": str(project.status),
                "description": str(project.description),
                "tech_stack": [str(tech) for tech in project.tech_stack],
                "created_at": str(project.created_at)
            }
        return serialized_projects


#PROJECT ASSIGNMENTS

class Project_assignmments(Base):
    __tablename__ = "project_assignments"

    id = Column(UUID, primary_key=True, nullable=False)
    proj_id = Column(UUID, ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    proj_manager_id = Column(UUID, nullable=False)
    proposal = Column(Boolean, nullable=False)
    deallocated = Column(Boolean, nullable=False)
    dealloc_reason = Column(String, nullable=False)
    work_hours = Column(INTEGER, nullable=False)
    comment = Column(String, nullable=False)

    @staticmethod
    def serialize_project_assignments(project_assignments):
        serialize_project_assignments = {}
        for project_assignment in project_assignments:
            serialize_project_assignments[str(project_assignment.id)] = {
                "id": str(project_assignment.id),
                "proj_id": str(project_assignment.proj_id),
                "proj_manager_id": str(project_assignment.proj_manager_id),
                "proposal": str(project_assignment.proposal),
                "deallocated": str(project_assignment.deallocated),
                "dealloc_reason": str(project_assignment.dealloc_reason),
                "work_hours": str(project_assignment.work_hours),
                "comment": str(project_assignment.comment)
            }
        return serialize_project_assignments

#PROJECTS MEMBERS

class Project_members(Base):
    __tablename__ = "project_members"

    user_id = Column(UUID, ForeignKey("users.id"),primary_key=True, nullable=False)
    proj_id = Column(UUID, ForeignKey("projects.id"), nullable=False)

    @staticmethod
    def serialize_project_members(project_members):
        serialize_project_members = []
        for project_member in project_members:
            project_member = {
                "user_id": str(project_member.user_id),
                "proj_id": str(project_member.proj_id),
            }
            serialize_project_members.append(project_member)
        return serialize_project_members

#USER TEAM ROLES
class  User_team_roles(Base):
    __tablename__ = "user_team_roles"

    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True, nullable=False)
    role_id = Column(UUID, ForeignKey("team_roles.id"), nullable=False)
    proposal = Column(Boolean, nullable=False)
    @staticmethod
    def serialize_user_team_roles(user_team_roles):
        serialize_user_team_roles = []
        for user_team_role in user_team_roles:
            user_team_role = {
                "user_id": str(user_team_role.user_id),
                "role_id": str(user_team_role.role_id),
                "proposal": str(user_team_role.proposal)
            }
            serialize_user_team_roles.append(user_team_role)
        return serialize_user_team_roles

#PROJECT TECH STACK SKILLS

class Project_tech_stack_skills(Base):
    __tablename__ = "project_tech_stack_skills"

    proj_id = Column(UUID, ForeignKey("projects.id"), primary_key=True, nullable=False)
    skill_id = Column(UUID, ForeignKey("skills.id"), nullable=False)
    @staticmethod
    def serialize_project_tech_stack_skills(project_tech_stack_skills):
        serialize_project_tech_stack_skill = []
        for project_tech_stack_skill in project_tech_stack_skills:
            project_tech_stack_skill = {
                "skill_id": str(project_tech_stack_skill.skill_id),
                "proj_id": str(project_tech_stack_skill.proj_id)
            }
            serialize_project_tech_stack_skill.append(project_tech_stack_skill)
        return serialize_project_tech_stack_skill

#PROJECT NEEDED ROLES

class Project_needed_roles(Base):
    __tablename__ = "project_needed_roles"

    proj_id = Column(UUID, ForeignKey("projects.id"), primary_key=True, nullable=False)
    role_id = Column(UUID, ForeignKey("team_roles.id"), nullable=False)
    count = Column(INTEGER, nullable=False)
    @staticmethod
    def serialize_project_needed_roles(project_needed_roles):
        serialize_project_needed_roles = []
        for project_needed_role in project_needed_roles:
            project_needed_role = {
                "role_id": str(project_needed_role.role_id),
                "proj_id": str(project_needed_role.proj_id),
                "count": str(project_needed_role.count)
            }
            serialize_project_needed_roles.append(project_needed_role)
        return serialize_project_needed_roles

