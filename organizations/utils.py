from uuid import uuid4
from database.db import db


def get_organizations():
    organizations = db.get_organizations()
    return organizations

def get_organizations_skills(organization_id):
    skills = db.get_skills()
    returned_skills = []
    skill_categories = db.get_skill_categories()
    departments = db.get_department()
    users = db.get_users()
    for key in skills:
        skill = skills[key]
        if skill.get("org_id") == organization_id:
            modified_skill = skill
            for user in users:
                current_user = users[user]
                if modified_skill["author_id"] == current_user.get("id"):
                    modified_skill["author_name"] = current_user.get("name")
                    break
            for department in departments:
                current_department = departments[department]
                if modified_skill["dept_id"] == current_department.get("id"):
                    modified_skill["dept_name"] = current_department.get("name")
                    break
            for skill_category in skill_categories:
                current_skill_category = skill_categories[skill_category]
                if modified_skill["category_id"] == current_skill_category.get("id"):
                    modified_skill["category_name"] = current_skill_category.get("name")
                    break
            returned_skills.append(modified_skill)
    print(returned_skills)
    return returned_skills



def create_organization(data):
    organization_data = data.model_dump()
    organization_id = str(uuid4())
    organization_data["id"] = organization_id

    db.create_organization(name=organization_data.get("name"),
                           admin_id=organization_data.get("admin_id"),
                           hq_address=organization_data.get("hq_address"),
                           created_at=organization_data.get("created_at"),
                           organization_id=organization_id)

    return organization_data
