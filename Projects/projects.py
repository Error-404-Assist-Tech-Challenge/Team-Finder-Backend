from fastapi import APIRouter, Depends
from Projects.models import Project, DeleteProject, UpdateProject
from Projects.utils import create_project, get_projects, delete_project, update_project, get_user_projects
from auth import AuthHandler

projects_router = APIRouter()
auth_handler = AuthHandler()


@projects_router.post("/api/project")
def create_projects_route(projects_data: Project, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_project(projects_data, user_id)


# Get all projects

@projects_router.get("/api/projects")
def projects_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_projects(user_id)


@projects_router.delete("/api/project")
def delete_projects_route(deleted_project: DeleteProject, user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_project(deleted_project, user_id)


@projects_router.put("/api/project")
def update_projects_route(modified_project: UpdateProject, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_project(modified_project, user_id)


@projects_router.get("/api/project")
def projects_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_projects(user_id)


@projects_router.get("/api/projects/user")
def user_projects(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_user_projects(user_id)
