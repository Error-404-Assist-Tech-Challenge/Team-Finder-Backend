from uuid import uuid4
from database.db import db


def get_skill_categories():
    skill_categories = db.get_skill_categories()
    return skill_categories


def create_skill_categories(data):
    skill_categories_data = data.model_dump()
    skill_categories_id = str(uuid4())
    skill_categories_data["id"] = skill_categories_id

    db.create_skill_categories(name=skill_categories_data.get("name"),
                           dept_id=skill_categories_data.get("dept_id"),
                           created_at=skill_categories_data.get("created_at"),
                           skill_categories_id=skill_categories_id)

    return skill_categories_data
