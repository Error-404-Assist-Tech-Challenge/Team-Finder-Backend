from database.models import Admin
from sqlalchemy.exc import SQLAlchemyError


# ADMIN UTILS
def create_admin(session, name, email, password, admin_id, oname, address):
    try:
        obj = Admin(name=name, email=email, password=password, id=admin_id, oname=oname, address=address)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_admin(session):
    admins = session.query(Admin).all()
    return Admin.serialize_employees(admins)
