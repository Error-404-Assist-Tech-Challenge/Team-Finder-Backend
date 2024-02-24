from uuid import uuid4
from database.db import db


def get_departaments():
    departaments = db.get_organization()
    return departaments


def create_departament(data):
    departament_data = data.model_dump()
    departament_id = str(uuid4())
    departament_data["id"] = departament_id

    db.create_departament(name=departament_data.get("name"),
                       org_id=departament_data.get("org_id"), manager_id=departament_data.get("manager_id"), departament_id=departament_id)

    return departament_data
