from sqlalchemy.exc import SQLAlchemyError

from database.departments_member.models import Department_members


def create_department_member(session, dept_id, user_id, department_member_id):
    try:
        obj = Department_members(dept_id=dept_id, user_id=user_id, id=department_member_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_department_members(session):
    members = session.query(Department_members).all()
    return Department_members.serialize_department_members(members)
