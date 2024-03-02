from fastapi import APIRouter, Depends
from Skills.models import Skills
from Skills.utils import create_skills, get_skills
from auth import AuthHandler

auth_handler = AuthHandler()
skills_router = APIRouter()


@skills_router.post("/api/skills", response_model=Skills)
def create_skills_route(skills_data: Skills):
    return create_skills(skills_data)


@skills_router.get("/api/skills")
def skills_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_skills(user_id)
