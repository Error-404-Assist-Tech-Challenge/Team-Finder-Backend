from sqlalchemy.exc import SQLAlchemyError

from database.organization_members.models import Organization_members


def create_organization_member(session, org_id, user_id):
    try:
        obj = Organization_members(org_id=org_id, user_id=user_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_organization_members(session):
    try:
        members = session.query(Organization_members).all()
        return Organization_members.serialize_organization_members(members)
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
        return error
