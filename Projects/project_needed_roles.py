from fastapi import APIRouter
from Projects.models import Project_needed_roles
from Projects.utils import create_project_needed_role, get_project_needed_roles

project_needed_roles_router = APIRouter()


@project_needed_roles_router.post("/api/projects/project_needed_roles", response_model=Project_needed_roles)
def create_project_needed_role_route(project_needed_roles_data: Project_needed_roles):
    return create_project_needed_role(project_needed_roles_data)



@project_needed_roles_router.get("/api/projects/project_needed_roles")
def project_needed_roles_get():
    return get_project_needed_roles()
