from fastapi import APIRouter, Depends
from Projects.models import Projects
from Projects.utils import create_projects, get_projects
from auth import AuthHandler

projects_router = APIRouter()
auth_handler = AuthHandler()

@projects_router.post("/api/projects", response_model=Projects)
def create_projects_route(projects_data: Projects):
    return create_projects(projects_data)


@projects_router.get("/api/projects")
def projects_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_projects(user_id)


@projects_router.get("/api/project")
def projects_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_projects(user_id)
