from sqlalchemy.exc import SQLAlchemyError

from database.Projects.models import *
from database.Skills.models import Skill_proposals

# PROJECTS


def create_project(session, project_id, org_id, name, period, start_date, deadline_date, status, description, manager_id, created_at, can_be_deleted, tech_stack):
    try:
        obj = Projects(id=project_id,
                       org_id=org_id,
                       name=name,
                       period=period,
                       start_date=start_date,
                       deadline_date=deadline_date,
                       status=status,
                       can_be_deleted=can_be_deleted,
                       description=description,
                       manager_id=manager_id,
                       tech_stack=tech_stack,
                       created_at=created_at)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def remove_project_manager_id(session, proj_id, manager_id):
    try:
        project = session.query(Projects).filter(Projects.proj_id == proj_id).first()
        if project:
            project.manager_id = manager_id
            session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def update_project(session, project_id, name, period, start_date, deadline_date, status, description, can_be_deleted, tech_stack):
    try:
        project = session.query(Projects).filter(Projects.id == project_id).first()
        if project:
            project.name = name
            project.period = period
            project.start_date = start_date
            project.deadline_date = deadline_date
            project.status = status
            project.description = description
            project.tech_stack = tech_stack
            project.can_be_deleted = can_be_deleted
            session.commit()
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


def delete_project(session, project_id):
    try:
        project = session.query(Projects).filter(Projects.id == project_id).first()
        if project:
            session.delete(project)
            session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def project_info(session, proj_id):
    try:
        project = session.query(Projects).filter(Projects.id == proj_id).first()
        return project.serialize()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_manager_projects(session, user_id):
    try:
        projects = session.query(Projects).filter(Projects.manager_id == user_id).all()
        return Projects.serialize_projects(projects)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


# PROJECT ASSIGNMENTS
def create_project_assignments(session, project_assignments_id, user_id, proj_id, proposal, deallocated, dealloc_reason, work_hours, comment, org_id, role_ids):
    try:
        obj = Project_assignments(id=project_assignments_id,
                                  user_id=user_id,
                                  proj_id=proj_id,
                                  org_id=org_id,
                                  role_ids=role_ids,
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


def update_project_assignments(session, assignment_id, role_ids = None, work_hours = None, comment = None, proposal = None, deallocated = None, dealloc_reason = None):
    try:
        project_assignment = session.query(Project_assignments).filter(Project_assignments.id == assignment_id).first()
        if project_assignment:
            if comment and role_ids and work_hours:
                project_assignment.role_ids = role_ids
                project_assignment.work_hours = work_hours
                project_assignment.comment = comment

            project_assignment.proposal = proposal
            project_assignment.deallocated = deallocated
            project_assignment.dealloc_reason = dealloc_reason

        project_proposal = session.query(Skill_proposals).filter(Skill_proposals.assignment_id == assignment_id).first()
        if project_proposal:
            if comment and role_ids:
                project_proposal.role_ids = role_ids
                # project_proposal.work_hours = work_hours
                project_proposal.comment = comment
            project_proposal.dealloc_reason = dealloc_reason

        return project_assignment.serialize()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def delete_project_assignments(session, assignment_id):
    try:
        assignment_proposal = session.query(Skill_proposals).filter(Skill_proposals.assignment_id == assignment_id).first()
        if assignment_proposal:
            session.delete(assignment_proposal)

        assignment = session.query(Project_assignments).filter(Project_assignments.id == assignment_id).first()
        if assignment:
            session.delete(assignment)

        return assignment.serialize()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def delete_project_assignment_proposal(session, assignment_id):
    try:
        assignment_proposal = session.query(Skill_proposals).filter(Skill_proposals.assignment_id == assignment_id).first()
        if assignment_proposal:
            session.delete(assignment_proposal)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def accept_project_assignment(session, assignment_id):
    try:
        project_assignment = session.query(Project_assignments).filter(Project_assignments.id == assignment_id).first()
        if project_assignment:
            project_assignment.proposal = False
            project_assignment.deallocated = False

        project_proposal = session.query(Skill_proposals).filter(Skill_proposals.assignment_id == assignment_id).first()
        if project_proposal:
            session.delete(project_proposal)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_project_assignments(session, org_id):
    try:
        project_assignments = session.query(Project_assignments).filter(Project_assignments.org_id == org_id).all()
        return Project_assignments.serialize_project_assignments(project_assignments)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_project_assigned_members(session, proj_id):
    try:
        members = session.query(Project_assignments).filter(Project_assignments.proj_id == proj_id).all()
        return Project_assignments.serialize_project_assignments(members)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_assignment_info(session, id):
    try:
        assignment_proposal = session.query(Project_assignments).filter(Project_assignments.id == id).first()
        return assignment_proposal.serialize()
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

# USER TEAM ROLES


def create_user_team_role(session, user_id, role_id):
    try:
        obj = User_team_roles(user_id=user_id, role_id=role_id)
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


def create_project_tech_stack_skill(session, proj_id, skill_id, minimum_level):
    try:
        id = uuid.uuid4()
        obj = Project_tech_stack_skills(id=id, proj_id=proj_id, skill_id=skill_id, minimum_level=minimum_level)

        session.add(obj)
        return obj.serialize()
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


def delete_required_skills(session, project_id):
    try:
        required_skills = session.query(Project_tech_stack_skills).filter(Project_tech_stack_skills.proj_id == project_id).all()
        if required_skills:
            for skill in required_skills:
                session.delete(skill)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def delete_required_skill(session, project_id, skill_id):
    try:
        required_skill = session.query(Project_tech_stack_skills).filter(Project_tech_stack_skills.proj_id == project_id,
                                                                         Project_tech_stack_skills.skill_id == skill_id).first()
        if required_skill:
            session.delete(required_skill)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def update_project_tech_stack_skill(session, proj_id, skill_id, minimum_level):
    try:
        project_tech_stack_skill = session.query(Project_tech_stack_skills).filter(Project_tech_stack_skills.proj_id == proj_id,
                                                                                   Project_tech_stack_skills.skill_id == skill_id).first()

        if project_tech_stack_skill:
            project_tech_stack_skill.minimum_level = minimum_level
            session.commit()

        return project_tech_stack_skill
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


def update_project_needed_role(session, id, count):
    try:
        project_needed_role = session.query(Project_needed_roles).filter(Project_needed_roles.id == id).first()
        if project_needed_role:
            project_needed_role.count = count
            session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_project_needed_role(session, role_id, proj_id):
    try:
        project_needed_role = session.query(Project_needed_roles).filter(Project_needed_roles.role_id == role_id,
                                                                         Project_needed_roles.proj_id == proj_id).first()
        return project_needed_role.serialize()
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


def delete_project_needed_roles(session, project_id):
    try:
        project_needed_roles = session.query(Project_needed_roles).filter(Project_needed_roles.proj_id == project_id).all()
        for role in project_needed_roles:
            session.delete(role)
            session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error
