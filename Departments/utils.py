from uuid import uuid4
from database.db import db

# DEPARTMENTS
def get_departments(user_id):
    users = db.get_users()
    organization_id = users[user_id].get("org_id")

    departments = db.get_department(organization_id)
    returned_departments = []

    for department_id, department_info in departments.items():
        department_members = db.get_department_members(department_id)

        manager_id = department_info.get("manager_id")

        if manager_id is not None:
            manager_name = users.get(manager_id, {}).get("name", "")
        else:
            manager_name = ""

        department_info["department_members"] = department_members
        department_info["manager_name"] = manager_name

        returned_departments.append(department_info)

    sorted_departments = sorted(returned_departments, key=lambda x: x['name'])

    return sorted_departments


def get_managed_department(user_id):
    user_data = db.get_user(user_id)
    org_id = user_data.get("org_id")

    departments = db.get_department(org_id)

    for key in departments:
        if departments[key].get("manager_id") == user_id:
            return {"name": departments[key].get("name")}



def create_department(data, user_id):
    users = db.get_users()
    organization_id = users[user_id].get("org_id")

    department_data = data.model_dump()
    department_id = str(uuid4())
    department_data["id"] = department_id
    name = department_data.get("name")
    created_at = department_data.get("created_at")
    db.create_department(name=name,
                         org_id=organization_id,
                         created_at=created_at,
                         department_id=department_id)

    returned_data = get_departments(user_id)

    return returned_data


def update_department(data, user_id):
    department_data = data.model_dump()

    db.update_department(name=department_data.get("name"),
                         manager_id=department_data.get("manager_id"),
                         dept_id=department_data.get("dept_id"))

    returned_data = get_departments(user_id)

    return returned_data


def delete_department(data, user_id):
    removed_department = data.model_dump().get("dept_id")

    db.delete_department(dept_id=removed_department)
    db.delete_department_members(dept_id=removed_department)
    db.delete_department_skills(dept_id=removed_department)

    returned_data = get_departments(user_id)

    return returned_data


def get_departments_managers(user_id):
    dep_role = "fa124499-1762-4f3b-8a61-712307e1677a"
    managers_with_department = []
    managers_available = []

    users = db.get_users()
    organization_id = users[user_id].get("org_id")

    org_user_roles = db.get_org_user_roles(organization_id)
    org_departments = db.get_department(organization_id)

    for department in org_departments:
        current_department = org_departments[department]
        managers_with_department.append(current_department.get("manager_id"))

    for user in org_user_roles:
        if (user.get("user_id") not in managers_with_department) and user.get("role_id") == dep_role:
            user_name = users[user.get("user_id")].get("name")
            returned_body = {
                "value": user.get("user_id"),
                "label": user_name
            }
            managers_available.append(returned_body)
    return managers_available


def get_projects_department(user_id): # Endpoint where department manager can see the projects if one of  his members are on the project
    returned_projects = []
    department_members = []
    user = db.get_user(user_id)
    organization_id = user.get("org_id")
    departments = db.get_department(organization_id)
    for department in departments:
        current_department = departments[department]
        if current_department.get("manager_id") == user_id:
            current_department_members = db.get_department_members(current_department.get("id"))
            for member in current_department_members:
                department_members.append(member.get("user_id"))

    project_members = db.get_project_members()
    for member in project_members:
        if member.get("user_id") in department_members:
            returned_projects.append(db.get_projects_id(member.get("proj_id")))

    return returned_projects


# DEPARTMENT_MEMBERS
def get_department_members(user_id):
    user_data = db.get_user(user_id)
    org_id = user_data.get("org_id")
    departments = db.get_department(org_id)

    for department in departments:
        current_department = departments[department]
        if current_department.get("manager_id") == user_id:
            department_members = db.get_department_members(department)

            for member in department_members:
                member_skill_names = []
                member_skills = db.get_user_skills(member.get("user_id"))
                org_skills = db.get_skills(org_id)

                for skill in member_skills:
                    org_skill = org_skills.get(skill.get("skill_id"))

                    if org_skill:
                        member_skill_names.append(org_skill.get("name"))

                member["skills"] = member_skill_names

            return department_members


def get_available_department_members(user_id):
    unavailable_users = []
    available_users = []
    users = db.get_users()
    organization_id = users[user_id].get("org_id")
    org_users = db.get_organization_users(organization_id)
    org_departments = db.get_department(organization_id)
    for department in org_departments:
        dep_members = db.get_department_members(department)
        for member in dep_members:
            unavailable_users.append(member.get("user_id"))
    for user in org_users:
        current_user = org_users[user]
        if current_user.get("id") not in unavailable_users:
            available_users.append(current_user)
    return available_users


def create_department_member(data, user_id):
    member_data = data.model_dump()
    member_id = member_data.get("user_id")
    organization_id = db.get_user(user_id).get("org_id")
    org_departments = db.get_department(organization_id)
    for department in org_departments:
        current_department = org_departments[department]
        if current_department.get("manager_id") == user_id:
            db.create_department_member(dept_id=current_department.get("id"),
                                        user_id=member_id)

    returned_data = get_department_members(user_id)
    return returned_data


def delete_department_member(data, user_id):
    user_info = data.model_dump()
    delete_user = user_info.get("user_id")

    organization_id = db.get_user(user_id).get("org_id")
    org_departments = db.get_department(organization_id)

    for department in org_departments:
        current_department = org_departments[department]
        department_members = db.get_department_members(current_department.get("id"))
        for member in department_members:
            member_id = member.get("user_id")
            if member_id == str(delete_user):
                db.delete_department_member(user_id=member_id,
                                            dept_id=member.get("dept_id"))

                returned_data = get_department_members(user_id)
                return returned_data

