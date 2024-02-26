from uuid import uuid4
from database.db import db


def get_skills():
    skills = db.get_skills()
    return skills


def create_skills(data):
    skill_data = data.model_dump()
    skill_id = str(uuid4())
    skill_data["id"] = skill_id

    db.create_skill(name=skill_data.get("name"),
                   dept_id=skill_data.get("dept_id"),
                   description=skill_data.get("description"),
                   category_id=skill_data.get("category_id"),
                    created_at=skill_data.get("created_at"),
                    skill_id=skill_id)

    return skill_data
