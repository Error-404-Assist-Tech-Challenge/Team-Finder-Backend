from sqlalchemy.exc import SQLAlchemyError
from database.roles.models import Role

def create_role(session, name, role_id):
    try:
        obj = Role(name=name, role_id=role_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
        return error

def get_roles(session):
    try:
        roles = session.query(Role).all()
        return Role.serialize_roles(roles)
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
        return error
