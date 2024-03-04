from uuid import uuid4
from database.db import db

#DEPARTMENTS
def get_departments(user_id):
    users = db.get_users()
    organization_id = users[user_id]
    departments = db.get_department(organization_id)
    return departments


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

#DEPARTMENT_MEMBERS
def get_department_members():
    members = db.get_department_members()
    return members


def create_department_member(data):
    department_member_data = data.model_dump()
    department_member_id = str(uuid4())
    department_member_data["id"] = department_member_id

    db.create_department_member(dept_id=department_member_data.get("dept_id"), user_id=department_member_data.get("user_id"), department_member_id=department_member_id)
    return department_member_data

