from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Skills.models import Skills, Update_skill, Put_Notifications, Notification, Proposal, EmployeeProposal, AcceptEmployeeProposal, DeleteEmployeeProposal
from Skills.utils import create_skills, get_skills, update_skill_proposal, get_skill_proposals, get_department_notifications, update_department_notifications, get_employee_skill_proposals, delete_employee_skill_proposal, accept_employee_skill_proposal
from auth import AuthHandler

auth_handler = AuthHandler()
skills_router = APIRouter(tags=["Skills"])


@skills_router.post("/api/skills", response_model=Skills)
def create_skills_route(skills_data: Skills):
    return create_skills(skills_data)


@skills_router.get("/api/skills")
def skills_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_skills(user_id)


@skills_router.put("/api/skills/proposal", response_model=List[Proposal])
def skill_proposal_update(skills_proposal_data: Update_skill, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_skill_proposal(skills_proposal_data, user_id)


@skills_router.get("/api/skills/proposal", response_model=List[Proposal])
def skill_proposal_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_skill_proposals(user_id)


@skills_router.get("/api/skills/employee_proposals", response_model=List[EmployeeProposal])
def employee_skill_proposal_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_employee_skill_proposals(user_id)


@skills_router.post("/api/skills/employee_proposals", response_model=List[EmployeeProposal])
def employee_skill_proposal_accept(proposal_data: AcceptEmployeeProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    returned_data, error = accept_employee_skill_proposal(proposal_data, user_id)
    if error:
        raise HTTPException(status_code=409, detail=error)
    return returned_data


@skills_router.delete("/api/skills/employee_proposals", response_model=List[EmployeeProposal])
def employee_skill_proposal_delete(proposal_data: DeleteEmployeeProposal, user_id: str = Depends(auth_handler.auth_wrapper)):
    returned_data, error = delete_employee_skill_proposal(proposal_data, user_id)
    if error:
        raise HTTPException(status_code=409, detail=error)
    return returned_data


@skills_router.get("/api/skills/proposal/unread", response_model=List[Notification])
def get_notifications(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_department_notifications(user_id)


@skills_router.put("/api/skills/proposal/unread", response_model=List[Notification])
def update_notifications(data: Put_Notifications, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_department_notifications(data, user_id)
