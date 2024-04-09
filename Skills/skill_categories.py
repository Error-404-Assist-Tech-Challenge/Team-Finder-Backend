from fastapi import APIRouter, Depends
from typing import List
from Skills.models import SkillCategory, DeleteSkillCategory, UpdateSkillCategory, SkillCategoriesResponse
from Skills.utils import create_skill_category, delete_skill_category, get_skill_categories, update_skill_category, get_unused_skill_categories
from auth import AuthHandler

auth_handler = AuthHandler()
skill_categories_router = APIRouter(tags=["Skills"])


@skill_categories_router.post("/api/skills/categories", response_model=List[SkillCategoriesResponse])
def create_skill_categories_route(skill_categories_data: SkillCategory, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_skill_category(skill_categories_data, user_id)


@skill_categories_router.get("/api/skills/categories", response_model=List[SkillCategoriesResponse])
def skill_categories_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_skill_categories(user_id)


@skill_categories_router.delete("/api/skills/categories", response_model=List[SkillCategoriesResponse])
def skill_categories_get(skill_categories_data: DeleteSkillCategory, user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_skill_category(skill_categories_data, user_id)


# @skill_categories_router.get("/api/skills/categories/unused")
# def unused_skill_categories_get(user_id: str = Depends(auth_handler.auth_wrapper)):
#     return get_unused_skill_categories(user_id)


@skill_categories_router.put("/api/skills/categories", response_model=List[SkillCategoriesResponse])
def update_skill_category_route(update_skill_category_data: UpdateSkillCategory, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_skill_category(update_skill_category_data, user_id)
