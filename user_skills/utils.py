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

def get_skills_by_users_id(user_id):
    user_skills = db.get_user_skills()
    skills = db.get_skills()

    users_skills_list = []
    for key in user_skills:
        user_skill = user_skills[key]
        if user_skill.get("user_id") == user_id:
            user_skill_id = user_skill.get("skill_id")
            skill_name = skills.get(user_skill_id, {}).get("name")
            user_skill["skill_name"] = skill_name
            users_skills_list.append(user_skill)
    return users_skills_list

def update_user_skills(data):
    user_skill_data = data.model_dump()
    db.update_user_skill(user_id=user_skill_data.get("user_id"),
                          skill_id=user_skill_data.get("skill_id"),
                          level=user_skill_data.get("level"),
                          experience=user_skill_data.get("experience"))

    return user_skill_data

