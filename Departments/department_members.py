from fastapi import APIRouter, Depends
from Departments.models import DepartmentMember, Delete_member
from Departments.utils import create_department_member, get_department_members, get_available_department_members, delete_department_member
from auth import AuthHandler

auth_handler = AuthHandler()
department_members_router = APIRouter()


@department_members_router.post("/api/departments/members", response_model=DepartmentMember)
def create_department_member_route(department_member_data: DepartmentMember):
    return create_department_member(department_member_data)


@department_members_router.get("/api/departments/members")
def department_members_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_department_members(user_id)


@department_members_router.delete("/api/departments/members")
def department_member_remove(remove_data: Delete_member, user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_department_member(remove_data, user_id)


@department_members_router.get("/api/departments/members/available")
def available_department_members_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_available_department_members(user_id)
