from fastapi import APIRouter
from Projects.models import Projects
from Projects.utils import create_projects, get_projects

projects_router = APIRouter()


@projects_router.post("/api/projects", response_model=Projects)
def create_projects_route(projects_data: Projects):
    return create_projects(projects_data)


@projects_router.get("/api/projects")
def projects_get():
    return get_projects()
