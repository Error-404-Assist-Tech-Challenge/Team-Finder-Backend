from uuid import uuid4

from database.db import db
from datetime import datetime, time


# PROJECTS

def get_projects(user_id):
    returned_user_projects = []
    organization_id = db.get_user(user_id).get("org_id")
    projects = db.get_org_projects(organization_id)
    for project in projects:
        current_project = projects[project]
        project_id = current_project.get("id")
        if str(current_project.get("manager_id")) == str(user_id):
            # Getting tech stack skills names
            tech_stack = db.get_project_tech_stack_skills(project_id, organization_id)
            current_project["tech_stack"] = tech_stack

            # Getting team role names
            team_role = db.get_project_needed_roles(project_id, organization_id)
            current_project["team_role"] = team_role
            del current_project["org_id"]
            returned_user_projects.append(current_project)
    return returned_user_projects


def create_projects(data):
    project_data = data.model_dump()
    project_id = str(uuid4())
    project_data["id"] = project_id

    # Create project info
    db.create_project(project_id=project_id,
                      org_id=project_data.get("org_id"),
                      manager_id=project_data.get("manager_id"),
                      name=project_data.get("name"),
                      period=project_data.get("period"),
                      start_date=project_data.get("start_date"),
                      deadline_date=project_data.get("deadline_date"),
                      status=project_data.get("status"),
                      description=project_data.get("description"),
                      created_at=project_data.get("created_at"))
    # Create project tech stack
    db.create_project_tech_stack_skills(project_id, project_data.get("tech_stack"))

    # Create team roles needed
    team_roles_needed = project_data.get("team_roles")
    for team_role in team_roles_needed:
        project_needed_role_id = str(uuid4())
        db.create_project_needed_roles(project_needed_role_id, project_id, team_role.get("role_id"), team_role.get("count"))

    return project_data

# PROJECTS MEMBERS

def get_project_members():
    project_members = db.get_project_member()
    return project_members


def create_project_member(data):
    project_member_data = data.model_dump()
    db.create_project_member(user_id=project_member_data.get("user_id"),
                             proj_id=project_member_data.get("proj_id"))
    return project_member_data

# PROJECTS ASSIGNMENTS
def get_project_assignments():
    project_assignments = db.get_project_assignments()
    return project_assignments


def create_project_assignment(data):
    project_assignments_data = data.model_dump()
    project_assignments_id = str(uuid4())
    project_assignments_data["id"] = project_assignments_id

    db.create_project_assignment(proj_id=project_assignments_data.get("proj_id"),
                                 user_id=project_assignments_data.get("user_id"),
                                 proj_manager_id=project_assignments_data.get("proj_manager_id"),
                                 proposal=project_assignments_data.get("proposal"),
                                 deallocated=project_assignments_data.get("deallocated"),
                                 dealloc_reason=project_assignments_data.get("dealloc_reason"),
                                 work_hours=project_assignments_data.get("work_hours"),
                                 comment=project_assignments_data.get("comment"),
                                 project_assignments_id=project_assignments_id)

    return project_assignments_data

# USER TEAM ROLES
def get_user_team_roles():
    user_team_roles = db.get_user_team_roles()
    return user_team_roles


def create_user_team_role(data):
    user_team_role_data = data.model_dump()
    db.create_user_team_role(user_id=user_team_role_data.get("user_id"),
                             role_id=user_team_role_data.get("role_id"),
                             proposal=user_team_role_data.get("proposal"))
    return user_team_role_data

# PROJECT TECH STACK SKILLS

def get_project_tech_stack_skills():
    project_tech_stack_skills = db.get_project_tech_stack_skills()
    return project_tech_stack_skills


def create_project_tech_stack_skill(data):
    project_tech_stack_skill = data.model_dump()
    db.create_project_tech_stack_skills(proj_id=project_tech_stack_skill.get("proj_id"),
                                        tech_stack=project_tech_stack_skill.get("tech_stack"))
    return project_tech_stack_skill


# PROJECT NEEDED ROLES
def get_project_needed_roles():
    project_needed_roles = db.get_project_needed_roles()
    return project_needed_roles


def create_project_needed_role(data):
    project_needed_role = data.model_dump()
    db.create_project_needed_roles(proj_id=project_needed_role.get("proj_id"),
                                   role_id=project_needed_role.get("role_id"),
                                   count=project_needed_role.get("count"))
    return project_needed_role

