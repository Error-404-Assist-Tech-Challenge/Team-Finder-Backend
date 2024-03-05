from fastapi import APIRouter, Depends
from Departments.models import Department, Modified_department
from Departments.utils import create_department, get_departments, get_departments_managers
from auth import AuthHandler

departments_router = APIRouter()
auth_handler = AuthHandler()


@departments_router.post("/api/departments", response_model=Department)
def create_department_route(department_data: Department, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_department(department_data, user_id)


@departments_router.get("/api/departments")
def departments_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_departments(user_id)

@departments_router.put("/api/departments")
def departments_get(department_data: Department, user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_departments(user_id)


@departments_router.get("/api/departments/managers")
def departments_get_managers(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_departments_managers(user_id)
