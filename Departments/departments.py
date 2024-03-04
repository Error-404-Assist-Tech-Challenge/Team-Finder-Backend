from fastapi import APIRouter, Depends
from Departments.models import Department
from Departments.utils import create_department, get_departments
from auth import AuthHandler

departments_router = APIRouter()
auth_handler = AuthHandler()

@departments_router.post("/api/departments", response_model=Department)
def create_department_route(department_data: Department):
    return create_department(department_data)


@departments_router.get("/api/departments")
def departments_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_departments(user_id)
