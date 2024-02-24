from uuid import uuid4
from database.db import db


def get_users():
    employees = db.get_users()
    return employees


def create_users(data):
    users_data = data.model_dump()
    users_id = str(uuid4())
    users_data["id"] = users_id

    db.create_users(name=users_data.get("name"), email=users_data.get("email"),
                       password=users_data.get("password"), users_id=users_id)

    return users_data
