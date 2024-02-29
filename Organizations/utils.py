from uuid import uuid4
from database.db import db
from datetime import datetime, timedelta
import secrets


#USER_ROLES
def get_user_roles(user_id):
    user_roles = db.user_roles_get(user_id)
    return user_roles


def create_user_role(data):
    user_role_data = data.model_dump()
    db.create_user_role(user_id=user_role_data.get("user_id"),
                        role_id=user_role_data.get("role_id"))

    return user_role_data


#ORGANIZATIONS
def get_organizations():
    organizations = db.get_organizations()
    return organizations


def get_organizations_skills(user_id):
    returned_skills = []
    users = db.get_users()
    organization_id = users[user_id].get("org_id")

    skills = db.get_skills(organization_id)
    skill_categories = db.get_skill_categories(organization_id)
    departments = db.get_department_skills_names(organization_id)

    for skill in skills:

        modified_skill = skills[skill]
        modified_skill["dept_name"] = []
        for user in users:
            current_user = users[user]
            if modified_skill.get("author_id") == current_user.get("id"):
                modified_skill["author_name"] = current_user.get("name")

        for department in departments:
            current_department = departments[department]
            current_department_id = current_department.get("dept_id")
            current_skill_department_ids = modified_skill.get("dept_id")
            for department_id in current_skill_department_ids:
                if department_id == current_department_id:
                    modified_skill["dept_name"].append(current_department.get("dept_name"))

        for skill_category in skill_categories:
            current_skill_category = skill_categories[skill_category]
            current_skill_category_id = skill_categories[skill_category].get("id")
            if modified_skill.get("category_id") == current_skill_category_id:
                modified_skill["category_name"] = current_skill_category.get("name")
        returned_skills.append(modified_skill)
    return returned_skills


def create_organization(data):
    organization_data = data.model_dump()
    organization_id = str(uuid4())
    organization_data["id"] = organization_id

    db.create_organization(name=organization_data.get("name"),
                           hq_address=organization_data.get("hq_address"),
                           created_at=organization_data.get("created_at"),
                           organization_id=organization_id)

    return organization_data


#ORGANIZATION_ROLES
def get_organization_roles():
    user_roles = db.get_organization_roles()
    return user_roles


def create_organization_role(data):
    organization_role_data = data.model_dump()
    db.create_organization_role(id=organization_role_data.get("id"),
                        name=organization_role_data.get("name"))

    return organization_role_data


#TEAM_ROLES
def get_team_roles():
    team_roles = db.get_team_roles()
    return team_roles


def create_team_role(data):
    team_role_data = data.model_dump()
    db.create_team_role(id=team_role_data.get("id"),
                        org_id=team_role_data.get("org_id"),
                        name=team_role_data.get("name"))

    return team_role_data


#SIGNUP_TOKENS
def create_signup_token(org_id):
    format = "%Y-%m-%d %H:%M:%S"
    current_time = datetime.utcnow().strftime(format)
    expires_at = datetime.strptime(current_time, format) + timedelta(hours=12)
    id = secrets.token_urlsafe(16)
    token = db.create_signup_token(id, org_id, expires_at)
    return token


def get_organization_signup_tokens(org_id):
    tokens = db.get_org_signup_tokens(org_id)
    return tokens
