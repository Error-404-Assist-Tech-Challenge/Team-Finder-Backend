from uuid import uuid4
from database.db import db


# DEPARTMENTS
def get_departments(user_id):
    users = db.get_users()
    organization_id = users[user_id].get("org_id")

    departments = db.get_department(organization_id)
    all_dep_members = db.get_department_members(organization_id)
    returned_departments = []
    for department in departments:
        current_department = departments[department]
        department_members = []
        for dep_member in all_dep_members:
            member_dept_id = dep_member.get("dept_id")
            if member_dept_id == department:
                department_members.append(dep_member.get("user_name"))
        current_department["department_members"] = department_members
        current_department["manager_name"] = users[current_department.get("manager_id")].get("name")
        returned_departments.append(current_department)
    return returned_departments


def create_department(data):
    department_data = data.model_dump()
    department_id = str(uuid4())
    department_data["id"] = department_id

    db.create_department(name=department_data.get("name"),
                         org_id=department_data.get("org_id"),
                         manager_id=department_data.get("manager_id"),
                         created_at=department_data.get("created_at"),
                         department_id=department_id)

    return department_data

# DEPARTMENT_MEMBERS
def get_department_members(user_id):
    users = db.get_users()
    organization_id = users[user_id].get("org_id")
    members = db.get_department_members(organization_id)
    return members


def create_department_member(data):
    department_member_data = data.model_dump()

    db.create_department_member(dept_id=department_member_data.get("dept_id"),
                                user_id=department_member_data.get("user_id"))
    return department_member_data

