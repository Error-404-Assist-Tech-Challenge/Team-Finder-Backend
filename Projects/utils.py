from uuid import uuid4

from database.db import db
from datetime import datetime, timedelta
from Skills.utils import get_skill_proposals


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
            del current_project["created_at"], current_project["manager_id"],
    sorted_projects = sorted(returned_user_projects, key=lambda x: x["name"])
    return sorted_projects


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
                      created_at=project_data.get("created_at"),
                      can_be_deleted=True)
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
    status = project_data.get("status")
    if str(status) in ["In Progress", "Closed", "Closing"]:
        can_be_deleted = False
        # Update project
        db.update_project(name=project_data.get("name"),
                          project_id=project_id,
                          period=project_data.get("period"),
                          start_date=project_data.get("start_date"),
                          deadline_date=project_data.get("deadline_date"),
                          status=status,
                          description=project_data.get("description"),
                          created_at=project_data.get("created_at"),
                          can_be_deleted=can_be_deleted)
    else:
        db.update_project(name=project_data.get("name"),
                          project_id=project_id,
                          period=project_data.get("period"),
                          start_date=project_data.get("start_date"),
                          deadline_date=project_data.get("deadline_date"),
                          status=status,
                          description=project_data.get("description"),
                          created_at=project_data.get("created_at"),
                          can_be_deleted=True)

    # Update tech stack skills
    db.update_project_tech_stack_skills(project_id, project_data.get("tech_stack"))

    # Update project needed roles
    team_roles_needed = project_data.get("team_roles")
    db.delete_project_needed_roles(project_id)
    for team_role in team_roles_needed:
        project_needed_role_id = str(uuid4())
        db.create_project_needed_roles(project_needed_role_id, project_id, team_role.get("role_id"), team_role.get("count"))
    return get_projects(user_id)

# EMPLOYEE PROJECT


def get_user_projects(user_id):
    active = []
    past = []
    organization_id = db.get_user(user_id).get("org_id")
    project_assignments = db.get_project_assignments(organization_id)
    for assign in project_assignments:
        if str(assign.get("user_id")) == user_id:
            project_id = assign.get("proj_id")
            # See if user is active in a project
            if assign.get("proposal") is False and assign.get("deallocated") is False:
                project_info = db.get_project_info(project_id)
                assign["project_name"] = project_info.get("name")
                assign["start_date"] = project_info.get("start_date")
                assign["deadline_date"] = project_info.get("deadline_date")
                assign["status"] = project_info.get("status")
                assign["description"] = project_info.get("description")
                assign["technology_stack"] = db.get_project_tech_stack_skills(project_id, organization_id)
                assign["role_names"] = db.get_project_needed_roles_names(project_id, organization_id)
                active.append(assign)
            elif assign.get("proposal") is False and assign.get("deallocated") is True:
                project_info = db.get_project_info(project_id)
                assign["project_name"] = project_info.get("name")
                assign["start_date"] = project_info.get("start_date")
                assign["deadline_date"] = project_info.get("deadline_date")
                assign["status"] = project_info.get("status")
                assign["description"] = project_info.get("description")
                assign["technology_stack"] = db.get_project_tech_stack_skills(project_id, organization_id)
                assign["role_names"] = db.get_project_needed_roles_names(project_id, organization_id)
                past.append(assign)

    returned_body = {
        "active": active,
        "past": past
    }
    return returned_body

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
    org_team_roles = db.get_team_roles(org_id)

    stack_skill_ids = []
    for skill in tech_stack_skills:
        stack_skill_ids.append(skill.get("skill_id"))

    eligible_employees = []
    active_employees = []
    proposed_employees = []
    deallocated_employees = []

    users_skills = db.get_users_skills()
    for employee_skill in users_skills:
        employee_data = db.get_user(employee_skill.get("user_id"))

        if employee_data.get("org_id") == org_id and employee_skill.get("user_id") != user_id:
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

                employee_skill["name"] = employee_data.get("name")

                eligible_employees.append(employee_skill)

    user_ids_to_remove = []
    for employee in eligible_employees:
        employee_id = employee.get("user_id")
        employee["dept_name"] = ""
        employee["roles"] = []

        # Check if the employee is assigned to a department
        for dept_member in dept_members:
            if dept_member.get("user_id") == employee_id:
                dept_info = db.get_department_info(dept_member.get("dept_id"))
                employee["dept_name"] = dept_info.get("name")

        # Check if the employee manages a department
        if not employee["dept_name"]:
            for key in org_departments:
                if org_departments[key].get("manager_id") == employee_id:
                    employee["dept_name"] = org_departments[key].get("name")

        deadlines = []
        work_hours = 0
        # Check each project assignment for the employee
        # to determine their status and get their work hours
        for assignment in proj_assignments:
            if assignment.get("user_id") == employee_id:

                if not assignment.get("proposal") and assignment.get("deallocated"):
                    pass
                else:
                    work_hours += int(assignment.get("work_hours"))

                if assignment.get("proj_id") == proj_id:

                    if assignment.get("proposal") and not assignment.get("deallocated"):
                        employee["comment"] = assignment.get("comment")
                        work_hours -= int(assignment.get("work_hours"))
                        employee["proposed_work_hours"] = assignment.get("work_hours")
                        proposed_employees.append(employee)
                        user_ids_to_remove.append(employee_id)

                    if not assignment.get("proposal") and assignment.get("deallocated"):
                        deallocated_employees.append(employee)

                    if assignment.get("proposal") and assignment.get("deallocated"):
                        employee["deallocate_proposal"] = True
                        employee["deallocate_comment"] = assignment.get("dealloc_reason")
                        active_employees.append(employee)
                        user_ids_to_remove.append(employee_id)

                    if not assignment.get("proposal") and not assignment.get("deallocated"):
                        active_employees.append(employee)
                        user_ids_to_remove.append(employee_id)

                    employee["current_work_hours"] = assignment.get("work_hours")
                    employee["assignment_id"] = assignment.get("id")

                    user_role_ids = assignment.get("role_ids")

                    # Get employee team roles
                    for role_id in user_role_ids:
                        employee_role_name = org_team_roles.get(role_id).get("name")
                        employee["roles"].append({"id": role_id, "name": employee_role_name})

                    if employee in proposed_employees:
                        employee["proposed_roles"] = user_role_ids

                else:
                    employee_project_info = db.get_projects_id(assignment.get("proj_id"))[0]
                    proj_deadline = employee_project_info.get("deadline_date")

                    deadlines.append(proj_deadline)

        # Get the nearest assigned project deadline
        nearest_deadline_str = ""
        if deadlines:
            deadlines = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in deadlines]
            nearest_deadline = min(deadlines, key=lambda date: abs(date - datetime.now()))
            nearest_deadline_str = nearest_deadline.strftime('%Y-%m-%d')

        employee["deadline"] = nearest_deadline_str

        employee["work_hours"] = work_hours

        del employee["created_at"], employee["skill_id"], employee["experience"], employee["level"]

    active_employees = sorted(active_employees, key=lambda x: x["name"])
    proposed_employees = sorted(proposed_employees, key=lambda x: x["name"])
    deallocated_employees = sorted(deallocated_employees, key=lambda x: x["name"])

    potential_employees = [employee for employee in eligible_employees if employee.get('user_id') not in user_ids_to_remove]

    returned_data = {"active": active_employees, "proposed": proposed_employees, "past": deallocated_employees, "new": potential_employees}

    return returned_data


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
    deallocation_data = data.model_dump()
    project_assignments_id = str(uuid4())
    deallocation_data["id"] = project_assignments_id
    proj_id = deallocation_data.get("proj_id")
    organization_id = db.get_user(user_id).get("org_id")
    assigned_user_id = deallocation_data.get("user_id")
    org_departments = db.get_department(db.get_user(user_id).get("org_id"))
    dept_members = db.get_all_department_members()

    dept_id = None
    # Check if the employee is assigned to a department
    for dept_member in dept_members:
        if str(dept_member.get("user_id")) == str(assigned_user_id):
            dept_id = dept_member.get("dept_id")

    # Check if the employee manages a department
    if not dept_id:
        for key in org_departments:
            if str(org_departments[key].get("manager_id")) == str(assigned_user_id):
                dept_id = key

    db.create_project_assignment(proj_id=proj_id,
                                 user_id=assigned_user_id,
                                 org_id=organization_id,
                                 role_ids=deallocation_data.get("role_ids"),
                                 proposal=True,
                                 deallocated=False,
                                 dealloc_reason=deallocation_data.get("dealloc_reason"),
                                 work_hours=deallocation_data.get("work_hours"),
                                 comment=deallocation_data.get("comment"),
                                 project_assignments_id=project_assignments_id)
    db.create_project_assignment_proposal(id=str(uuid4()),
                                          dept_id=dept_id,
                                          role_ids=deallocation_data.get("role_ids"),
                                          comment=deallocation_data.get("comment"),
                                          user_id=assigned_user_id,
                                          assignment_id=project_assignments_id,
                                          proposal=True,
                                          deallocated=False,
                                          read=False)
    return search_employees(proj_id, user_id)


def update_project_assignment(data, user_id):
    update_data = data.model_dump()
    proj_id = update_data.get("proj_id")

    db.update_project_assignment(assignment_id=update_data.get("assignment_id"),
                                 role_ids=update_data.get("role_ids"),
                                 work_hours=update_data.get("proposed_work_hours"),
                                 comment=update_data.get("comment"))

    return search_employees(proj_id, user_id)


def delete_project_assignment(data, user_id):
    delete_data = data.model_dump()
    proj_id = delete_data.get("proj_id")

    db.delete_project_assignment(delete_data.get("assignment_id"))

    return search_employees(proj_id, user_id)


def create_project_deallocation(data, user_id):
    deallocation_data = data.model_dump()
    project_assignment_id = deallocation_data.get("assignment_id")
    proj_id = deallocation_data.get("proj_id")
    org_id = db.get_user(user_id).get("org_id")
    assigned_user_id = deallocation_data.get("user_id")
    org_departments = db.get_department(org_id)
    org_assignments = db.get_project_assignments(org_id)
    dept_members = db.get_all_department_members()

    dept_id = None
    # Check if the employee is assigned to a department
    for dept_member in dept_members:
        if str(dept_member.get("user_id")) == str(assigned_user_id):
            dept_id = dept_member.get("dept_id")

    # Check if the employee manages a department
    if not dept_id:
        for key in org_departments:
            if str(org_departments[key].get("manager_id")) == str(assigned_user_id):
                dept_id = key

    role_ids = []
    for assignment in org_assignments:
        if str(assignment.get("id")) == str(project_assignment_id):
            role_ids = assignment.get("role_ids")

    db.update_project_assignment(assignment_id=project_assignment_id,
                                 proposal=True,
                                 deallocated=True,
                                 dealloc_reason=deallocation_data.get("comment"))

    db.create_project_assignment_proposal(id=str(uuid4()),
                                          dept_id=dept_id,
                                          role_ids=role_ids,
                                          dealloc_reason=deallocation_data.get("comment"),
                                          user_id=assigned_user_id,
                                          assignment_id=project_assignment_id,
                                          proposal=True,
                                          deallocated=True,
                                          read=False)

    return search_employees(proj_id, user_id)


def update_project_deallocation(data, user_id):
    update_data = data.model_dump()
    proj_id = update_data.get("proj_id")

    db.update_project_assignment(assignment_id=update_data.get("assignment_id"),
                                 proposal=True,
                                 deallocated=True,
                                 dealloc_reason=update_data.get("comment"))

    return search_employees(proj_id, user_id)


def delete_project_deallocation(data, user_id):
    delete_data = data.model_dump()
    proj_id = delete_data.get("proj_id")

    db.update_project_assignment(assignment_id=delete_data.get("assignment_id"),
                                 proposal=False,
                                 deallocated=False,
                                 dealloc_reason="")

    db.delete_project_assignment_proposal(assignment_id=delete_data.get("assignment_id"))

    return search_employees(proj_id, user_id)


def manage_proposal(data, user_id):
    manage_data = data.model_dump()
    assignment_id = manage_data.get("assignment_id")
    type = manage_data.get("type")
    action = manage_data.get("action")

    if action == "Accept":
        if type == "Assignment":
            db.accept_project_assignment(assignment_id)
        elif type == "Deallocation":
            db.update_project_assignment(assignment_id=manage_data.get("assignment_id"),
                                         proposal=False,
                                         deallocated=True)
            db.delete_project_assignment_proposal(assignment_id=assignment_id)
    elif action == "Reject":
        if type == "Assignment":
            db.delete_project_assignment(assignment_id)
        elif type == "Deallocation":
            db.update_project_assignment(assignment_id=manage_data.get("assignment_id"),
                                         proposal=False,
                                         deallocated=False,
                                         dealloc_reason="")
            db.delete_project_assignment_proposal(assignment_id=assignment_id)

    return get_skill_proposals(user_id)


# USER TEAM ROLES
def get_user_team_roles():
    user_team_roles = db.get_user_team_roles()
    return user_team_roles


def create_user_team_role(data):
    user_team_role_data = data.model_dump()
    db.create_user_team_role(user_id=user_team_role_data.get("user_id"),
                             role_id=user_team_role_data.get("role_id"))
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

