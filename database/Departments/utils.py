from sqlalchemy.exc import SQLAlchemyError

from database.Departments.models import *


# DEPARTMENTS
def create_department(session, org_id, name, created_at, department_id):
    try:
        obj = Department(org_id=org_id, name=name, created_at=created_at, id=department_id)
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


def update_department(session, dept_id, name):
    try:
        department_info = session.query(Department).filter(
            Department.id == dept_id
        ).first()

        if department_info:
            department_info.name = name
            session.commit()
            return department_info
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        session.rollback()
        print(error)
        return error

def delete_department(session, dept_id):
    try:
        department_info = session.query(Department).filter(
            Department.id == dept_id
        ).first()

        if department_info:
            session.delete(department_info)
            session.commit()
            return department_info
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        session.rollback()
        print(error)
        return error

#DEPARTMENT_MEMBERS
def create_department_member(session, dept_id, user_id):
    try:
        obj = Department_members(dept_id=dept_id, user_id=user_id)
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

def delete_department_members(session, dept_id):
    try:
        members = session.query(Department_members).filter(Department_members.dept_id == dept_id).all()
        if members:
            for member in members:
                session.delete(member)
                session.commit()
        return members
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error
