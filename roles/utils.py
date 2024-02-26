from database.db import db


def get_roles():
    roles = db.get_roles()
    return roles


def create_role(data):
    role_data = data.model_dump()

    db.create_roles()

    return role_data
