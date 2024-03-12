from fastapi import APIRouter, Depends
from Projects.models import AssignmentProposal, UpdateAssignmentProposal, SearchResponse, DeleteAssignmentProposal
from Projects.utils import create_project_assignment, get_project_assignments, update_project_assignment, delete_project_assignment
from auth import AuthHandler

project_assignments_router = APIRouter()
auth_handler = AuthHandler()


@project_assignments_router.post("/api/projects/assignment_proposal", response_model=SearchResponse)
def create_project_assignments_route(project_assignments_data: AssignmentProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_project_assignment(project_assignments_data, user_id)


@project_assignments_router.put("/api/projects/assignment_proposal", response_model=SearchResponse)
def create_project_assignments_route(project_assignments_data: UpdateAssignmentProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_project_assignment(project_assignments_data, user_id)


@project_assignments_router.delete("/api/projects/assignment_proposal", response_model=SearchResponse)
def create_project_assignments_route(project_assignments_data: DeleteAssignmentProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_project_assignment(project_assignments_data, user_id)


@project_assignments_router.get("/api/projects/project_assignments")
def project_assignments_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_project_assignments(user_id)
