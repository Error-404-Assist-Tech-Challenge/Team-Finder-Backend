from sqlalchemy.exc import SQLAlchemyError

from database.organizations.models import Organization


def create_organization(session, admin_id, name, hq_address, created_at, organization_id):
    try:
        obj = Organization(admin_id=admin_id, name=name, hq_address=hq_address, created_at=created_at, id=organization_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_organizations(session):
    try:
        organizations = session.query(Organization).all()
        return Organization.serialize_organizations(organizations)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


