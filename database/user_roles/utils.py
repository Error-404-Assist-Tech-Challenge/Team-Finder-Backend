from sqlalchemy.exc import SQLAlchemyError
from database.user_roles.models import UserRole


def create_user_role(session, user_id, role_id):
    try:
        obj = UserRole(user_id=user_id, role_id=role_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_user_roles(session):
    try:
        user_roles = session.query(UserRole).all()
        return UserRole.serialize_user_roles(user_roles)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error
