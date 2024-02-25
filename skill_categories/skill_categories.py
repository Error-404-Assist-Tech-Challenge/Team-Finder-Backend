from fastapi import APIRouter
from skill_categories.models import Skill_categories
from skill_categories.utils import *

skill_categories_route = APIRouter()


@skill_categories_route.post("/api/skill_categories", response_model=Skill_categories)
def create_skill_categories_route(skill_categories_data: Skill_categories):
    return create_skill_categories(skill_categories_data)


@skill_categories_route.get("/api/skill_categories")
def skill_categories_get():
    return get_skill_categories()
