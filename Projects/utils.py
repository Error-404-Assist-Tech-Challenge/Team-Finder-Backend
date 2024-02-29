from uuid import uuid4

from database.db import db
from datetime import datetime, time


#PROJECTS

def get_projects():
    projects = db.get_projects()
    return projects


def create_projects(data):
    project_data = data.model_dump()
    project_id = str(uuid4())
    project_data["id"] = project_id

    start_date = project_data.get("start_date")
    start_date_iso = start_date.isoformat()

    deadline_date = project_data.get("deadline_date")
    deadline_date_iso = deadline_date.isoformat()

    db.create_project(name=project_data.get("name"),
                      start_date=start_date_iso,
                      deadline_date=deadline_date_iso,
                      status=project_data.get("status"),
                      period=project_data.get("period"),
                      description=project_data.get("description"),
                      tech_stack=project_data.get("tech_stack"),
                      created_at=project_data.get("created_at"),
                      org_id=project_data.get("org_id"),
                      project_id=project_id)

    return project_data

#PROJECTS MEMBERS

def get_project_members():
    project_members = db.get_project_member()
    return project_members


def create_project_member(data):
    project_member_data = data.model_dump()
    db.create_project_member(user_id=project_member_data.get("user_id"),
                             proj_id=project_member_data.get("proj_id"))
    return project_member_data

#PROJECTS ASSIGNMENTS

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

#USER TEAM ROLES

def get_user_team_roles():
    user_team_roles = db.get_user_team_roles()
    return user_team_roles


def create_user_team_role(data):
    user_team_role_data = data.model_dump()
    db.create_user_team_role(user_id=user_team_role_data.get("user_id"),
                                  role_id=user_team_role_data.get("role_id"),
                                  proposal=user_team_role_data.get("proposal"))
    return user_team_role_data

#PROJECT TECH STACK SKILLS

def get_project_tech_stack_skills():
    project_tech_stack_skills = db.get_project_tech_stack_skills()
    return project_tech_stack_skills


def create_project_tech_stack_skill(data):
    project_tech_stack_skill = data.model_dump()
    db.create_project_tech_stack_skills(proj_id=project_tech_stack_skill.get("proj_id"),
                                       skill_id=project_tech_stack_skill.get("skill_id"))
    return project_tech_stack_skill

#PROJECT NEEDED ROLES

def get_project_needed_roles():
    project_needed_roles = db.get_project_needed_roles()
    return project_needed_roles


def create_project_needed_role(data):
    project_needed_role = data.model_dump()
    db.create_project_needed_roles(proj_id=project_needed_role.get("proj_id"),
                                  role_id=project_needed_role.get("role_id"),
                                  count=project_needed_role.get("count"))
    return project_needed_role

