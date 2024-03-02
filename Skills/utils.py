from uuid import uuid4
from database.db import db

#SKILLS

def get_skills(user_id):
    users = db.get_users()
    organization_id = users[user_id]
    skills = db.get_skills(organization_id)
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
    all_users = db.get_users()
    organization_id = all_users[user_id].get("org_id")
    user_skills = db.get_user_skills(user_id)
    skills = db.get_skills(organization_id)
    skill_categories = get_skill_categories(organization_id)
    user_skills_list = []
    for user_skill in user_skills:
        if user_skill.get("user_id") == user_id:
            user_skill_id = user_skill.get("skill_id")
            if skills[user_skill_id]:
                skill = skills[user_skill_id]

                #Put skill category in user skills
                for skill_category in skill_categories:
                    current_skill_category = skill_categories[skill_category]
                    if current_skill_category.get("id") == skill.get("category_id"):
                        user_skill["category_name"] = current_skill_category.get("name")
                # Put name in user skills
                skill_name = skill.get("name")
                user_skill["skill_name"] = skill_name
                # Put description in user skills
                skill_description = skill.get("description")
                user_skill["skill_description"] = skill_description

                user_skills_list.append(user_skill)
    user_skills_list.sort(key=lambda x: x.get("skill_name", "").lower())
    return user_skills_list

def create_user_skills(data, user_id):
    user_skill_data = data.model_dump()
    db.create_user_skills(user_id=user_id,
                    skill_id=user_skill_data.get("skill_id"),
                    level="0",
                    experience="0",
                    created_at=user_skill_data.get("created_at"))

    return user_skill_data


def update_user_skills(data, user_id):
    user_skill_data = data.model_dump()
    db.update_user_skill(user_id=user_id,
                         skill_id=user_skill_data.get("skill_id"),
                         level=user_skill_data.get("level"),
                         experience=user_skill_data.get("experience"))
    updated_user_skills = user_skill_data
    return updated_user_skills

#SKILL_CATEGORIES

def get_skill_categories(organization_id):
    skill_categories = db.get_skill_categories(organization_id)
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

    db.skill_department_create(dept_id=department_skills_data.get("dept_id"), skill_id=department_skills_data.get("skill_id"))

    return department_skills_data

def update_department_skills(data):
    department_skills_data = data.model_dump()
    db.skill_department_update(dept_id=department_skills_data.get("dept_id"),
                               skill_id=department_skills_data.get("skill_id"),
                               new_dept_id=department_skills_data.get("new_dept_id"),
                               new_skill_id=department_skills_data.get("new_skill_id"))
    return department_skills_data
