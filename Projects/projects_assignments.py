from fastapi import APIRouter, Depends
from Projects.models import Project_assignments
from Projects.utils import create_project_assignment, get_project_assignments
from auth import AuthHandler

project_assignments_router = APIRouter()
auth_handler = AuthHandler()


@project_assignments_router.post("/api/projects/project_assignments", response_model=Project_assignments)
def create_project_assignments_route(project_assignments_data: Project_assignments, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_project_assignment(project_assignments_data, user_id)


@project_assignments_router.get("/api/projects/project_assignments")
def project_assignments_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_project_assignments(user_id)
