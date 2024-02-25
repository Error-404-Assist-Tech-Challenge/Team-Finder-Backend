from fastapi import APIRouter
from user_skills.models import UserSkills
from user_skills.utils import *

user_skills_router = APIRouter()


@user_skills_router.post("/api/user_skills", response_model=UserSkills)
def create_user_skill_route(user_skill_data: UserSkills):
    return create_user_skills(user_skill_data)


@user_skills_router.get("/api/user_skills")
def user_skills_get():
    return get_user_skills()
