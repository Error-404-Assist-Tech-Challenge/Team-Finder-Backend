from fastapi import APIRouter, Depends
from Projects.models import Projects
from Projects.utils import create_projects, get_projects, delete_project
from auth import AuthHandler

projects_router = APIRouter()
auth_handler = AuthHandler()


@projects_router.post("/api/projects")
def create_projects_route(projects_data: Projects, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_projects(projects_data, user_id)

# Get all projects


@projects_router.get("/api/projects")
def projects_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_projects(user_id)


@projects_router.delete("/api/project")
def delete_projects_route(user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_project(user_id)


@projects_router.get("/api/project")
def projects_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_projects(user_id)
