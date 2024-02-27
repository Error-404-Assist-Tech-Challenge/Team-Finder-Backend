from typing import List
from fastapi import APIRouter
from Skills.models import UserSkills, UpdateSkills
from Skills.utils import create_user_skills, get_skills_by_users_id, update_user_skills

user_skills_router = APIRouter()


@user_skills_router.post("/api/user_skills", response_model=UserSkills)
def create_user_skill_route(user_skill_data: UserSkills):
    return create_user_skills(user_skill_data)


@user_skills_router.get("/api/user_skills")
def user_skills_get(user_id: str):
    return get_skills_by_users_id(user_id)


@user_skills_router.put("/api/user_skills", response_model=UpdateSkills)
def updating_user_skills(user_skill_data: List[UpdateSkills]):
    return update_user_skills(user_skill_data)


