from fastapi import APIRouter, Depends
from typing import List
from Departments.models import DepartmentMember, CreateMember,DeleteMember
from Departments.utils import create_department_member, get_department_members, get_available_department_members, delete_department_member
from auth import AuthHandler

auth_handler = AuthHandler()
department_members_router = APIRouter()


@department_members_router.post("/api/departments/members", response_model=List[DepartmentMember])
def create_department_member_route(department_member_data: CreateMember, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_department_member(department_member_data, user_id)


@department_members_router.get("/api/departments/members", response_model=List[DepartmentMember])
def department_members_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_department_members(user_id)


@department_members_router.delete("/api/departments/members", response_model=List[DepartmentMember])
def department_member_remove(remove_data: DeleteMember, user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_department_member(remove_data, user_id)


@department_members_router.get("/api/departments/members/available")
def available_department_members_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_available_department_members(user_id)
