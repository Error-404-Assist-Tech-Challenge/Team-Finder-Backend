from fastapi import APIRouter
from departments.models import Department
from departments.utils import *

departments_router = APIRouter()


@departments_router.post("/api/departments", response_model=Department)
def create_department(department_data: Department):
    return create_department(department_data)


@departments_router.get("/api/departments")
def departments_get():
    return get_departments()
