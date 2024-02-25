from fastapi import APIRouter
from department_members.models import Department_member
from department_members.utils import create_department_member, get_department_members

department_members_router = APIRouter()


@department_members_router.post("/api/department_members", response_model=Department_member)
def create_department_member_route(department_member_data: Department_member):
    return create_department_member(department_member_data)


@department_members_router.get("/api/department_members")
def department_members_get():
    return get_department_members()
