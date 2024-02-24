from sqlalchemy.exc import SQLAlchemyError
from database.departaments.models import Departaments


def create_departament(session, org_id, name, manager_id, departament_id):
    try:
        obj = Departaments(org_id=org_id, name=name, manager_id=manager_id, id=departament_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_departament(session):
    departaments = session.query(Departaments).all()
    return Departaments.serialize_employees(departaments)