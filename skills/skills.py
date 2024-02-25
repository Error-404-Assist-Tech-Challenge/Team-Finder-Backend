from fastapi import APIRouter
from skills.models import Skills
from skills.utils import *

skills_router = APIRouter()


@skills_router.post("/api/skills", response_model=Skills)
def create_skills_route(skills_data: Skills):
    return create_skills(skills_data)


@skills_router.get("/api/skills")
def skills_get():
    return get_skills()
