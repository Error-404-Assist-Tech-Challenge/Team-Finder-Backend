from fastapi import APIRouter
from Projects.models import Project_assignments
from Projects.utils import create_project_assignment, get_project_assignments

project_assignments_router = APIRouter()


@project_assignments_router.post("/api/project_assignments", response_model=Project_assignments)
def create_project_assignments_route(project_assignments_data: Project_assignments):
    return create_project_assignment(project_assignments_data)


@project_assignments_router.get("/api/project_assignments")
def project_assignments_get():
    return get_project_assignments()
