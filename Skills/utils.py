from uuid import uuid4
from database.db import db

#SKILLS

def get_skills():
    skills = db.get_skills()
    return skills


def create_skills(data):
    skill_data = data.model_dump()
    skill_id = str(uuid4())
    skill_data["id"] = skill_id

    db.create_skill(name=skill_data.get("name"),
                    description=skill_data.get("description"),
                    category_id=skill_data.get("category_id"),
                    created_at=skill_data.get("created_at"),
                    author_id=skill_data.get("author_id"),
                    org_id=skill_data.get("org_id"),
                    skill_id=skill_id)

    return skill_data

#USER_SKILLS

def get_skills_by_users_id(user_id):
    user_skills = db.get_user_skills()
    skills = db.get_skills()
    user_skills_list = []
    for key in user_skills:
        user_skill = user_skills[key]
        if user_skill.get("user_id") == user_id:
            user_skill_id = user_skill.get("skill_id")
            skill_name = skills.get(user_skill_id, {}).get("name")
            user_skill["skill_name"] = skill_name
            user_skills_list.append(user_skill)
    user_skills_list.sort(key=lambda x: x.get("skill_name", "").lower())
    return user_skills_list

def create_user_skills(data):
    user_skill_data = data.model_dump()
    db.create_user_skills(user_id=user_skill_data.get("user_id"),
                    skill_id=user_skill_data.get("skill_id"),
                    level=user_skill_data.get("level"),
                    created_at=user_skill_data.get("created_at"),
                    experience=user_skill_data.get("experience"))

    return user_skill_data


def update_user_skills(data):
    updated_user_skills = {}
    for user_skill_data in data:
        user_skill_dict = user_skill_data.model_dump()
        user_id = user_skill_dict.get("user_id")
        db.update_user_skill(user_id=user_id,
                             skill_id=user_skill_dict.get("skill_id"),
                             level=user_skill_dict.get("level"),
                             experience=user_skill_dict.get("experience"))
        updated_user_skills = user_skill_dict
    return updated_user_skills

#SKILL_CATEGORIES

def get_skill_categories(user_id):
    skill_categories = db.get_skill_categories(user_id)
    return skill_categories


def create_skill_categories(data):
    skill_categories_data = data.model_dump()
    skill_categories_id = str(uuid4())
    skill_categories_data["id"] = skill_categories_id

    db.create_skill_categories(name=skill_categories_data.get("name"),
                           org_id=skill_categories_data.get("org_id"),
                           created_at=skill_categories_data.get("created_at"),
                           skill_categories_id=skill_categories_id)

    return skill_categories_data

def update_skill_category(data):
    user_skill_category_dict = data.model_dump()
    db.update_skill_category(id=user_skill_category_dict.get("id"),
                         org_id=user_skill_category_dict.get("org_id"),
                         name=user_skill_category_dict.get("name"),
                         modified_at=user_skill_category_dict.get("modified_at"))
    return user_skill_category_dict

#DEPARTMENT_SKILLS

def get_department_skills():
    department_skills = db.get_department_skills()
    return department_skills


def create_department_skill(data):
    department_skills_data = data.model_dump()
    department_skills_id = str(uuid4())
    department_skills_data["id"] = department_skills_id

    db.create_department_skill(dept_id=department_skills_data.get("dept_id"),
                           skill_id=department_skills_data.get("skill_id"))

    return department_skills_data

