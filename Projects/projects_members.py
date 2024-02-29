from fastapi import APIRouter
from Projects.models import Project_members
from Projects.utils import create_project_member, get_project_members

project_members_router = APIRouter()


@project_members_router.post("/api/project_members", response_model=Project_members)
def create_project_members_route(project_members_data: Project_members):
    return create_project_member(project_members_data)


@project_members_router.get("/api/project_members")
def project_members_get():
    return get_project_members()
