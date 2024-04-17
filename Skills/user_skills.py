from typing import List
from fastapi import APIRouter, Depends
from Skills.models import UserSkills, UpdateSkills, RemoveSkill, SkillsResponse
from Skills.utils import create_user_skills, get_skills_by_users_id, update_user_skills, remove_user_skill
from auth import AuthHandler

auth_handler = AuthHandler()
user_skills_router = APIRouter(tags=["Skills"])


@user_skills_router.post("/api/skills/user")
async def create_user_skill_route(user_skill_data: UserSkills, user_id: str = Depends(auth_handler.auth_wrapper)):
    return await create_user_skills(user_skill_data, user_id)


@user_skills_router.get("/api/skills/user")
def user_skills_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_skills_by_users_id(user_id)


@user_skills_router.delete("/api/skills/user")
def user_skills_delete(user_skill_data: RemoveSkill, user_id: str = Depends(auth_handler.auth_wrapper)):
    return remove_user_skill(user_skill_data, user_id)


@user_skills_router.put("/api/skills/user")
def updating_user_skills(user_skill_data: UpdateSkills, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_user_skills(user_skill_data, user_id)


