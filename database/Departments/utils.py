from sqlalchemy.exc import SQLAlchemyError

from database.Departments.models import *

#DEPARTMENTS
def create_department(session, org_id, name, manager_id, created_at, department_id):
    try:
        obj = Department(org_id=org_id, name=name, manager_id=manager_id, created_at=created_at, id=department_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_department(session):
    try:
        departments = session.query(Department).all()
        return Department.serialize_departments(departments)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

#DEPARTMENT_MEMBERS
def create_department_member(session, dept_id, user_id, department_member_id):
    try:
        obj = Department_members(dept_id=dept_id, user_id=user_id, id=department_member_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_department_members(session):
    try:
        members = session.query(Department_members).all()
        return Department_members.serialize_department_members(members)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error
