from fastapi import APIRouter
from Skills.models import Skill_categories
from Skills.utils import create_skill_categories, get_skill_categories

skill_categories_router = APIRouter()


@skill_categories_router.post("/api/skills/categories", response_model=Skill_categories)
def create_skill_categories_route(skill_categories_data: Skill_categories):
    return create_skill_categories(skill_categories_data)


@skill_categories_router.get("/api/skills/categories")
def skill_categories_get(organization_id: str):
    return get_skill_categories(organization_id)
