from sqlalchemy.exc import SQLAlchemyError

from database.departments.models import Department


def create_department(session, org_id, name, manager_id, department_id):
    try:
        obj = Department(org_id=org_id, name=name, manager_id=manager_id, id=department_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_department(session):
    departments = session.query(Department).all()
    return Department.serialize_departments(departments)
