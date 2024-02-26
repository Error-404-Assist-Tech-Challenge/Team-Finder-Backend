from database.db import db


def get_user_skills():
    user_skills = db.get_user_skills()
    return user_skills


def create_user_skills(data):
    user_skill_data = data.model_dump()
    db.create_user_skills(user_id=user_skill_data.get("user_id"),
                    skill_id=user_skill_data.get("skill_id"),
                    level=user_skill_data.get("level"),
                    created_at=user_skill_data.get("created_at"),
                    experience=user_skill_data.get("experience"))

    return user_skill_data
