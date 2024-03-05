from uuid import uuid4
from database.db import db


# DEPARTMENTS
def get_departments(user_id):
    users = db.get_users()
    organization_id = users[user_id].get("org_id")

    departments = db.get_department(organization_id)
    returned_departments = []
    for department in departments:
        current_department = departments[department]
        current_department_manager = current_department.get("manager_id")
        current_department["department_members"] = db.get_department_members(department)
        if current_department_manager is None:
            current_department["manager_name"] = users[current_department_manager].get("name")
        else:
            current_department["manager_name"] = {}
        returned_departments.append(current_department)
    return returned_departments


def create_department(data, user_id):
    users = db.get_users()
    organization_id = users[user_id].get("org_id")

    department_data = data.model_dump()
    department_id = str(uuid4())
    department_data["id"] = department_id

    db.create_department(name=department_data.get("name"),
                         org_id=organization_id,
                         created_at=department_data.get("created_at"),
                         department_id=department_id)

    return department_data

def get_departments_managers(user_id):
    managers_with_department = []
    managers_available = []
    users = db.get_users()
    organization_id = users[user_id].get("org_id")
    org_users = db.get_organization_users(organization_id)
    org_departments = db.get_department(organization_id)
    for department in org_departments:
        current_department = org_departments[department]
        managers_with_department.append(current_department.get("manager_id"))

    for user in org_users:
        current_user = org_users[user]
        if current_user.get("id") not in managers_with_department:
            returned_body = {
                "label": current_user.get("id"),
                "value": current_user.get("name")
            }
            managers_available.append(returned_body)
    return managers_available



# DEPARTMENT_MEMBERS
def get_department_members(user_id):
    users = db.get_users()
    organization_id = users[user_id].get("org_id")
    departments = db.get_department(organization_id)
    for department in departments:
        current_department = departments[department]
        if current_department.get("manager_id") == user_id:
            return db.get_department_members(department)



def create_department_member(data):
    department_member_data = data.model_dump()

    db.create_department_member(dept_id=department_member_data.get("dept_id"),
                                user_id=department_member_data.get("user_id"))
    return department_member_data

