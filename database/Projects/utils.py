from sqlalchemy.exc import SQLAlchemyError

from database.Projects.models import *

# PROJECTS


def create_project(session, project_id, org_id, name, period, start_date, deadline_date, status, description, manager_id, created_at):
    try:
        obj = Projects(id=project_id,
                       org_id=org_id,
                       name=name,
                       period=period,
                       start_date=start_date,
                       deadline_date=deadline_date,
                       status=status,
                       description=description,
                       manager_id=manager_id,
                       created_at=created_at)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_projects(session):
    try:
        projects = session.query(Projects).all()
        return Projects.serialize_projects(projects)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


# PROJECT ASSIGNMENTS
def create_project_assignments(session, project_assignments_id, user_id, proj_id, proj_manager_id, proposal, deallocated, dealloc_reason, work_hours, comment):
    try:
        obj = Project_assignments(id=project_assignments_id,
                                   user_id=user_id,
                                   proj_id=proj_id,
                                   proj_manager_id=proj_manager_id,
                                   proposal=proposal,
                                   deallocated=deallocated,
                                   dealloc_reason=dealloc_reason,
                                   work_hours=work_hours,
                                   comment=comment)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_project_assignments(session):
    try:
        project_assignments = session.query(Project_assignments).all()
        return Project_assignments.serialize_project_assignments(project_assignments)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

# PROJECT MEMBERS


def create_project_members(session, user_id, proj_id):
    try:
        obj = Project_members(user_id=user_id,
                       proj_id=proj_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_project_members(session):
    try:
        project_members = session.query(Project_members).all()
        return Project_members.serialize_project_members(project_members)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

#USER TEAM ROLES

def create_user_team_role(session, user_id, role_id, proposal):
    try:
        obj = User_team_roles(user_id=user_id,
                       role_id=role_id,
                       proposal=proposal)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_user_team_roles(session):
    try:
        user_team_roles = session.query(User_team_roles).all()
        return User_team_roles.serialize_user_team_roles(user_team_roles)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

# PROJECT TECH STACK SKILLS


def create_project_tech_stack_skill(session, tech_stack, proj_id):
    try:
        obj = Project_tech_stack_skills(tech_stack=tech_stack,
                                        proj_id=proj_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_project_tech_stack_skills(session):
    try:
        project_tech_stack_skills = session.query(Project_tech_stack_skills).all()
        return Project_tech_stack_skills.serialize_project_tech_stack_skills(project_tech_stack_skills)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

# PROJECT NEEDED ROLES


def create_project_needed_role(session, proj_id, id, role_id, count):
    try:
        obj = Project_needed_roles(proj_id=proj_id,
                                   role_id=role_id,
                                   id=id,
                                   count=count)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_project_needed_roles(session):
    try:
        project_needed_roles = session.query(Project_needed_roles).all()
        return Project_needed_roles.serialize_project_needed_roles(project_needed_roles)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error