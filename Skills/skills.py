from fastapi import APIRouter, Depends
from Skills.models import Skills, Update_skill
from Skills.utils import create_skills, get_skills, update_skill_proposal, get_skill_proposals
from auth import AuthHandler

auth_handler = AuthHandler()
skills_router = APIRouter()


@skills_router.post("/api/skills", response_model=Skills)
def create_skills_route(skills_data: Skills):
    return create_skills(skills_data)


@skills_router.get("/api/skills")
def skills_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_skills(user_id)


@skills_router.put("/api/skills/proposal", response_model=Update_skill)
def skill_proposal_update(skills_proposal_data: Update_skill):
    return update_skill_proposal(skills_proposal_data)


@skills_router.get("/api/skills/proposal")
def skill_proposal_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_skill_proposals(user_id)
