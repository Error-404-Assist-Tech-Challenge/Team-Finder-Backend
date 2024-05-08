import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, INTEGER, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from database.db import Base

# PROJECTS


class Projects(Base):
    __tablename__ = "projects"

    id = Column(UUID, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    manager_id = Column(UUID, nullable=False)
    org_id = Column(UUID, ForeignKey("organizations.id"), nullable=False)
    period = Column(String, nullable=False)
    start_date = Column(TIMESTAMP, nullable=False)
    deadline_date = Column(TIMESTAMP, nullable=True)
    status = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    can_be_deleted = Column(Boolean, nullable=False)
    tech_stack = Column(ARRAY(String), nullable=False)

    @staticmethod
    def serialize_projects(projects):
        serialized_projects = {}
        for project in projects:
            serialized_projects[str(project.id)] = {
                "id": str(project.id),
                "name": str(project.name),
                "org_id": str(project.org_id),
                "manager_id": str(project.manager_id),
                "period": str(project.period),
                "start_date": str(project.start_date),
                "deadline_date": str(project.deadline_date),
                "status": str(project.status),
                "description": str(project.description),
                "created_at": str(project.created_at),
                "tech_stack": project.tech_stack,
                "can_be_deleted": str(project.can_be_deleted)
            }
        return serialized_projects

    def serialize(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "org_id": str(self.org_id),
            "manager_id": str(self.manager_id),
            "period": str(self.period),
            "start_date": str(self.start_date),
            "deadline_date": str(self.deadline_date),
            "status": str(self.status),
            "description": str(self.description),
            "tech_stack": self.tech_stack,
            "created_at": str(self.created_at),
            "can_be_deleted": self.can_be_deleted
        }


# PROJECT ASSIGNMENTS

class Project_assignments(Base):
    __tablename__ = "project_assignments"

    id = Column(UUID, primary_key=True, nullable=False)
    org_id = Column(UUID, ForeignKey("organizations.id"), nullable=False)
    proj_id = Column(UUID, ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    role_ids = Column(ARRAY(UUID), ForeignKey("team_roles.id"), nullable=False)
    proposal = Column(Boolean, nullable=False)
    deallocated = Column(Boolean, nullable=True)
    dealloc_reason = Column(String, nullable=True)
    work_hours = Column(INTEGER, nullable=False)
    comment = Column(String, nullable=False)

    @staticmethod
    def serialize_project_assignments(project_assignments):
        serialized_project_assignments = []
        for project_assignment in project_assignments:
            serialized_project_assignments.append({
                "id": str(project_assignment.id),
                "org_id": str(project_assignment.org_id),
                "user_id": str(project_assignment.user_id),
                "role_ids": [str(role) for role in project_assignment.role_ids],
                "proj_id": str(project_assignment.proj_id),
                "proposal": bool(project_assignment.proposal),
                "deallocated": bool(project_assignment.deallocated),
                "dealloc_reason": str(project_assignment.dealloc_reason),
                "work_hours": str(project_assignment.work_hours),
                "comment": str(project_assignment.comment)
            })
        return serialized_project_assignments

    def serialize(self):
        return {
            "id": str(self.id),
            "org_id": str(self.org_id),
            "user_id": str(self.user_id),
            "role_ids": [str(role) for role in self.role_ids],
            "proj_id": str(self.proj_id),
            "proposal": bool(self.proposal),
            "deallocated": bool(self.deallocated),
            "dealloc_reason": str(self.dealloc_reason),
            "work_hours": str(self.work_hours),
            "comment": str(self.comment)
        }

# PROJECTS MEMBERS


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

# USER TEAM ROLES


class User_team_roles(Base):
    __tablename__ = "user_team_roles"

    id = Column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    role_id = Column(UUID, ForeignKey("team_roles.id"), nullable=False)

    @staticmethod
    def serialize_user_team_roles(user_team_roles):
        serialize_user_team_roles = []
        for user_team_role in user_team_roles:
            user_team_role = {
                "id": str(user_team_role.id),
                "user_id": str(user_team_role.user_id),
                "role_id": str(user_team_role.role_id)
            }
            serialize_user_team_roles.append(user_team_role)
        return serialize_user_team_roles

# PROJECT TECH STACK SKILLS


class Project_tech_stack_skills(Base):
    __tablename__ = "project_tech_stack_skills"

    id = Column(UUID, primary_key=True, nullable=False, default=uuid.uuid4())
    proj_id = Column(UUID, ForeignKey("projects.id"), nullable=False)
    skill_id = Column(UUID, ForeignKey("skills.id"), nullable=False)
    minimum_level = Column(INTEGER, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "skill_id": self.skill_id,
            "proj_id": self.proj_id,
            "minimum_level": self.minimum_level
        }

    @staticmethod
    def serialize_project_tech_stack_skills(project_tech_stack_skills):
        serialize_project_tech_stack_skill = {}
        for project_tech_stack_skill in project_tech_stack_skills:
            serialize_project_tech_stack_skill[str(project_tech_stack_skill.id)] = {
                "skill_id": str(project_tech_stack_skill.skill_id),
                "proj_id": str(project_tech_stack_skill.proj_id),
                "minimum_level": int(project_tech_stack_skill.minimum_level)
            }
        return serialize_project_tech_stack_skill


# PROJECT NEEDED ROLES

class Project_needed_roles(Base):
    __tablename__ = "project_needed_roles"

    id = Column(UUID, primary_key=True, nullable=False)
    proj_id = Column(UUID, ForeignKey("projects.id"), nullable=False)
    role_id = Column(UUID, ForeignKey("team_roles.id"), nullable=False)
    count = Column(INTEGER, nullable=False)

    def serialize(self):
        return {
            "id": str(self.id),
            "count": str(self.count)
        }

    @staticmethod
    def serialize_project_needed_roles(project_needed_roles):
        serialize_project_needed_roles = {}
        for project_needed_role in project_needed_roles:
            serialize_project_needed_roles[str(project_needed_role.id)] = {
                "role_id": str(project_needed_role.role_id),
                "proj_id": str(project_needed_role.proj_id),
                "count": str(project_needed_role.count)
            }
        return serialize_project_needed_roles

