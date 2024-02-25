from database.db import db


def get_user_roles():
    user_roles = db.get_roles()
    return user_roles


def create_user_role(data):
    user_role_data = data.model_dump()

    db.create_user_role()

    return user_role_data
