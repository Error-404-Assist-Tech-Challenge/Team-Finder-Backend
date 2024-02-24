from fastapi import APIRouter
from employee.models import EmployeeCreate
from employee.utils import create_employee, get_employees

employee_router = APIRouter()


@employee_router.post("/api/employee", response_model=EmployeeCreate)
def employee_create(data: EmployeeCreate):
    return create_employee(data)

@employee_router.get("/api/employees/get")
def employees_get():
    return get_employees()
