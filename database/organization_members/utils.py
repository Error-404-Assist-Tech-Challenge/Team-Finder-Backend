from sqlalchemy.exc import SQLAlchemyError

from database.organization_members.models import Organization_members


def create_organization_member(session, org_id, user_id, organization_member_id):
    try:
        obj = Organization_members(org_id=org_id, user_id=user_id, id=organization_member_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_organization_members(session):
    members = session.query(Organization_members).all()
    return Organization_members.serialize_organization_members(members)
