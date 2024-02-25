from sqlalchemy.exc import SQLAlchemyError
from database.roles.models import Role


def get_roles(session):
    try:
        roles = session.query(Role).all()
        return Role.serialize_roles(roles)
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
        return error
