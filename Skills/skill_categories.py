from typing import List
from fastapi import APIRouter
from Skills.models import Skill_categories, Update_skill_category
from Skills.utils import create_skill_categories, get_skill_categories, update_skill_category

skill_categories_router = APIRouter()


@skill_categories_router.post("/api/skills/categories", response_model=Skill_categories)
def create_skill_categories_route(skill_categories_data: Skill_categories):
    return create_skill_categories(skill_categories_data)


@skill_categories_router.get("/api/skills/categories")
def skill_categories_get(user_id: str):
    return get_skill_categories(user_id)


@skill_categories_router.put("/api/skills/categories", response_model=Update_skill_category)
def update_skill_category_route(update_skill_category_data: Update_skill_category):
    return update_skill_category(update_skill_category_data)
