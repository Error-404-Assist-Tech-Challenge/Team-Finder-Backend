from uuid import uuid4

from database.db import db
from datetime import datetime, timedelta
from Organizations.utils import get_org_users


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
            team_role, available_roles = db.get_project_needed_roles(project_id, organization_id)
            current_project["team_role"] = team_role
            del current_project["org_id"]
            current_project["available_roles"] = available_roles
            returned_user_projects.append(current_project)

            # Getting project approved members
            members = db.get_project_approved_members(project_id)
            current_project["projects"] = members
    return returned_user_projects


def create_projects(data, user_id):
    project_data = data.model_dump()
    project_id = str(uuid4())
    project_data["id"] = project_id
    # Create project info
    db.create_project(project_id=project_id,
                      org_id=db.get_user(user_id).get("org_id"),
                      manager_id=user_id,
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

    return get_projects(user_id)


def delete_project(data, user_id):
    project_id = data.model_dump().get("proj_id")
    db.delete_project(project_id=project_id)
    return get_projects(user_id)


def update_project(data, user_id):
    project_data = data.model_dump()
    project_id = project_data.get("proj_id")
    # Update project
    db.update_project(name=project_data.get("name"),
                      project_id=project_id,
                      period=project_data.get("period"),
                      start_date=project_data.get("start_date"),
                      deadline_date=project_data.get("deadline_date"),
                      status=project_data.get("status"),
                      description=project_data.get("description"),
                      created_at=project_data.get("created_at"))

    # Update tech stack skills
    db.update_project_tech_stack_skills(project_id, project_data.get("tech_stack"))

    # Update project needed roles
    team_roles_needed = project_data.get("team_roles")
    db.delete_project_needed_roles(project_id)
    for team_role in team_roles_needed:
        project_needed_role_id = str(uuid4())
        db.create_project_needed_roles(project_needed_role_id, project_id, team_role.get("role_id"), team_role.get("count"))
        return get_projects(user_id)
# PROJECTS MEMBERS


def get_project_members():
    project_members = db.get_project_member()
    return project_members


def create_project_member(data):
    project_member_data = data.model_dump()
    db.create_project_member(user_id=project_member_data.get("user_id"),
                             proj_id=project_member_data.get("proj_id"))
    return project_member_data


def search_employees(proj_id, user_id):
    proj_id = str(proj_id)
    user_data = db.get_user(user_id)
    org_id = user_data.get("org_id")
    dept_members = db.get_all_department_members()
    org_departments = db.get_department(org_id)
    proj_assignments = db.get_project_assignments(org_id)
    tech_stack_skills = db.get_project_tech_stack_skills(org_id=org_id, proj_id=proj_id)

    stack_skill_ids = []
    for skill in tech_stack_skills:
        stack_skill_ids.append(skill.get("skill_id"))

    eligible_employees = []
    users_skills = db.get_users_skills()
    for employee_skill in users_skills:
        employee_data = db.get_user(employee_skill.get("user_id"))

        if employee_data.get("org_id") == org_id:
            # Check if employee has relevant skills for the project
            if employee_skill.get("skill_id") in stack_skill_ids:
                skill_data = db.get_skill(employee_skill.get("skill_id"))
                employee_skill["skills"] = []
                employee_skill["skills"].append({
                    "name": skill_data.get("name"),
                    "experience": employee_skill.get("experience"),
                    "level": employee_skill.get("level")
                })

                # Check if the employee is already eligible and append skill
                is_already_eligible = False
                for employee in eligible_employees:
                    if employee["user_id"] == employee_skill.get("user_id"):
                        employee["skills"].append({
                            "name": skill_data.get("name"),
                            "experience": employee_skill.get("experience"),
                            "level": employee_skill.get("level")
                        })
                        is_already_eligible = True
                if is_already_eligible:
                    continue

                is_assigned_to_project = False
                deadlines = []
                work_hours = 0

                # Check each project assignment for the employee
                # to determine if they are assigned to the current project
                # and get their work hours
                for assignment in proj_assignments:
                    if assignment.get("user_id") == employee_skill.get("user_id"):
                        if assignment.get("proj_id") == proj_id:
                            is_assigned_to_project = True
                        if not bool(assignment.get("proposal")) and not bool(assignment.get("deallocated")):
                            work_hours += int(assignment.get("work_hours"))

                        employee_project_info = db.get_projects_id(assignment.get("proj_id"))[0]
                        proj_deadline = employee_project_info.get("deadline_date")

                        deadlines.append(proj_deadline)


                # Get the nearest assigned project deadline
                nearest_deadline_str = ""
                if deadlines:
                    deadlines = [datetime.strptime(date, '%Y-%m-%d') for date in deadlines]
                    nearest_deadline = min(deadlines, key=lambda date: abs(date - datetime.now()))
                    nearest_deadline_str = nearest_deadline.strftime('%Y-%m-%d')

                employee_skill["deadline"] = nearest_deadline_str

                if is_assigned_to_project:
                    continue

                employee_skill["dept_name"] = ""
                # Check if the employee is assigned to a department
                for dept_member in dept_members:
                    if dept_member.get("user_id") == employee_skill.get("user_id"):
                        dept_info = db.get_department_info(dept_member.get("dept_id"))
                        employee_skill["dept_name"] = dept_info.get("name")

                # Check if the employee manages a department
                if not employee_skill["dept_name"]:
                    for key in org_departments:
                        if org_departments[key].get("manager_id") == employee_skill.get("user_id"):
                            employee_skill["dept_name"] = org_departments[key].get("name")

                employee_skill["work_hours"] = work_hours

                del employee_skill["created_at"], employee_skill["skill_id"], employee_skill["experience"], employee_skill["level"]
                employee_skill["name"] = employee_data.get("name")
                eligible_employees.append(employee_skill)

    sorted_data = sorted(eligible_employees, key=lambda x: x["name"])

    return sorted_data


# PROJECTS ASSIGNMENTS
def get_project_assignments(user_id):
    manager_projects_ids = []
    returned_project_assignments = []
    organization_id = db.get_user(user_id).get("org_id")
    project_assignments = db.get_project_assignments(organization_id)
    manager_projects = db.get_manager_projects(user_id)
    for project in manager_projects:
        manager_projects_ids.append(project)
    for assign in project_assignments:
        if str(assign.get("proj_id")) in manager_projects_ids:
            returned_project_assignments.append(assign)
    return returned_project_assignments


def create_project_assignment(data, user_id):
    project_assignments_data = data.model_dump()
    project_assignments_id = str(uuid4())
    project_assignments_data["id"] = project_assignments_id
    organization_id = db.get_user(user_id).get("org_id")
    db.create_project_assignment(proj_id=project_assignments_data.get("proj_id"),
                                 user_id=project_assignments_data.get("user_id"),
                                 org_id=organization_id,
                                 role_id=project_assignments_data.get("role_id"),
                                 proposal=False,
                                 deallocated=False,
                                 dealloc_reason=project_assignments_data.get("dealloc_reason"),
                                 work_hours=project_assignments_data.get("work_hours"),
                                 comment=project_assignments_data.get("comment"),
                                 project_assignments_id=project_assignments_id)
    db.create_project_assignment_proposal(id=str(uuid4()),
                                          dept_id=db.get_department_user(project_assignments_data.get("user_id")),
                                          role_id=project_assignments_data.get("role_id"),
                                          comment=project_assignments_data.get("comment"),
                                          user_id=project_assignments_data.get("user_id"),
                                          assignment_id=project_assignments_id,
                                          proposal=False,
                                          read=False)
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

