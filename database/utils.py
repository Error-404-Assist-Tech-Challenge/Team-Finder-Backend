from database.models import Employee
from sqlalchemy.exc import SQLAlchemyError


# EMPLOYEE UTILS
def create_employee(session, name, email, password, employee_id):
    try:
        obj = Employee(name=name, email=email, password=password, id=employee_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_employees(session):
    employees = session.query(Employee).all()
    return Employee.serialize_employees(employees)
