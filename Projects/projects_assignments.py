from fastapi import APIRouter, Depends
from Projects.models import AssignmentProposal, UpdateAssignmentProposal, DeallocationProposal, UpdateDeallocationProposal, DeleteDeallocationProposal, SearchResponse, DeleteAssignmentProposal, ManageProposal
from Projects.utils import create_project_assignment, get_project_assignments, update_project_assignment, delete_project_assignment, manage_proposal, create_project_deallocation, delete_project_deallocation, update_project_deallocation
from auth import AuthHandler

project_assignments_router = APIRouter(tags=["Projects"])
auth_handler = AuthHandler()


@project_assignments_router.post("/api/projects/assignment_proposal", response_model=SearchResponse)
async def create_project_assignments_route(project_assignments_data: AssignmentProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    return await create_project_assignment(project_assignments_data, user_id)


@project_assignments_router.put("/api/projects/assignment_proposal", response_model=SearchResponse)
def create_project_assignments_route(project_assignments_data: UpdateAssignmentProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_project_assignment(project_assignments_data, user_id)


@project_assignments_router.post("/api/projects/deallocation_proposal", response_model=SearchResponse)
async def create_project_deallocation_route(project_assignments_data: DeallocationProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    return await create_project_deallocation(project_assignments_data, user_id)


@project_assignments_router.put("/api/projects/deallocation_proposal", response_model=SearchResponse)
def create_project_deallocation_route(project_assignments_data: UpdateDeallocationProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_project_deallocation(project_assignments_data, user_id)


@project_assignments_router.delete("/api/projects/deallocation_proposal", response_model=SearchResponse)
def create_project_deallocation_route(project_assignments_data: DeleteDeallocationProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_project_deallocation(project_assignments_data, user_id)


@project_assignments_router.delete("/api/projects/assignment_proposal", response_model=SearchResponse)
def create_project_assignments_route(project_assignments_data: DeleteAssignmentProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_project_assignment(project_assignments_data, user_id)


@project_assignments_router.post("/api/projects/manage_proposal")
def manage_proposal_route(manage_proposal_data: ManageProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    return manage_proposal(manage_proposal_data, user_id)


@project_assignments_router.get("/api/projects/project_assignments")
def project_assignments_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_project_assignments(user_id)
