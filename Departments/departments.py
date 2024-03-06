from fastapi import APIRouter, Depends
from typing import List
from Departments.models import Department, DepartmentUpdate, Remove_department, DepartmentResponse
from Departments.utils import create_department, get_departments, get_departments_managers, update_department, delete_department, get_projects_department
from auth import AuthHandler

departments_router = APIRouter()
auth_handler = AuthHandler()


@departments_router.post("/api/departments", response_model=List[DepartmentResponse])
def create_department_route(department_data: Department, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_department(department_data, user_id)


@departments_router.get("/api/departments", response_model=List[DepartmentResponse])
def departments_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_departments(user_id)


@departments_router.put("/api/departments", response_model=List[DepartmentResponse])
def departments_update(department_data: DepartmentUpdate, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_department(department_data, user_id)


@departments_router.delete("/api/departments", response_model=List[DepartmentResponse])
def departments_delete(removed_dept: Remove_department, user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_department(removed_dept, user_id)


@departments_router.get("/api/departments/managers")
def departments_get_managers(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_departments_managers(user_id)

@departments_router.get("/api/department/projects")
def departments_get_projects(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_projects_department(user_id)
