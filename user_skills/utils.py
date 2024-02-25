from database.db import db


def get_user_skills():
    user_skills = db.get_user_skills()
    return user_skills


def create_user_skills(data):
    skills_data = data.model_dump()
    db.create_user_skills(user_id=skills_data.get("user_id"),
                    skill_id=skills_data.get("skill_id"),
                    level=skills_data.get("level"),
                    experience=skills_data.get("experience"))

    return skills_data
