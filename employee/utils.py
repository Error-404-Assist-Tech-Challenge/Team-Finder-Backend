from uuid import uuid4
from database.db import db


def get_employees():
    employees = db.get_employees()
    return employees


def create_employee(data):
    employee_data = data.model_dump()
    employee_id = str(uuid4())
    employee_data["id"] = employee_id

    db.create_employee(name=employee_data.get("name"), email=employee_data.get("email"),
                       password=employee_data.get("password"), employee_id=employee_id)

    return employee_data
