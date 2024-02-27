from fastapi import APIRouter
from Skills.models import Skills
from Skills.utils import create_skills, get_skills

skills_router = APIRouter()


@skills_router.post("/api/skills", response_model=Skills)
def create_skills_route(skills_data: Skills):
    return create_skills(skills_data)


@skills_router.get("/api/skills")
def skills_get():
    return get_skills()
