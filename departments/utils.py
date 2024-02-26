from uuid import uuid4
from database.db import db


def get_departments():
    departments = db.get_department()
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
