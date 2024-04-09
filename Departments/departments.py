from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Departments.models import Department, DepartmentUpdate, RemoveDepartment, DepartmentResponse, ManagedDepartment, DepartmentProjectsResponse
from Departments.utils import *
from auth import AuthHandler

departments_router = APIRouter(tags=["Departments"])
auth_handler = AuthHandler()


@departments_router.post("/api/departments", response_model=List[DepartmentResponse])
def create_department_route(department_data: Department, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_department(department_data, user_id)


@departments_router.get("/api/departments", response_model=List[DepartmentResponse])
def departments_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_departments(user_id)


@departments_router.get("/api/departments/managed", response_model=ManagedDepartment)
def department_managed_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    response, error = get_managed_department(user_id)
    if error:
        raise HTTPException(status_code=409, detail=error)
    return response


@departments_router.put("/api/departments", response_model=List[DepartmentResponse])
def departments_update(department_data: DepartmentUpdate, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_department(department_data, user_id)


@departments_router.delete("/api/departments", response_model=List[DepartmentResponse])
def departments_delete(removed_dept: RemoveDepartment, user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_department(removed_dept, user_id)


@departments_router.get("/api/departments/managers")
def departments_get_managers(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_departments_managers(user_id)


@departments_router.get("/api/departments/statistics")
def departments_get_statistics(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_department_statistics(user_id)


@departments_router.get("/api/department/projects", response_model=List[DepartmentProjectsResponse])
def departments_get_projects(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_projects_department(user_id)
