from sqlalchemy.exc import SQLAlchemyError
from database.organization.models import Organization


def create_organization(session, admin_id, name, hq_address, organization_id):
    try:
        obj = Organization(admin_id=admin_id, name=name, hq_address=hq_address, id=organization_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_organization(session):
    organizations = session.query(Organization).all()
    return Organization.serialize_employees(organizations)