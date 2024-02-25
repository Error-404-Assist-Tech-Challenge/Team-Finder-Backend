from uuid import uuid4
from database.db import db


def get_users():
    employees = db.get_users()
    return employees


def create_user(data):
    user_data = data.model_dump()
    user_id = str(uuid4())
    user_data["id"] = user_id

    db.create_users(name=user_data.get("name"),
                    email=user_data.get("email"),
                    password=user_data.get("password"),
                    user_id=user_id)

    return user_data
