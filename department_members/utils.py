from uuid import uuid4
from database.db import db


def get_department_members():
    members = db.get_department_members()
    return members


def create_department_member(data):
    department_member_data = data.model_dump()
    department_member_id = str(uuid4())
    department_member_data["id"] = department_member_id

    db.create_department_member(dept_id=department_member_data.get("dept_id"), user_id=department_member_data.get("user_id"), department_member_id=department_member_id)
    return department_member_data
