from uuid import uuid4
from database.db import db

#USER_ROLES
def get_user_roles():
    user_roles = db.get_roles()
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

def get_organizations_skills(organization_id):
    returned_skills = []

    skills = db.get_skills()
    skill_categories = db.get_skill_categories()
    departments = db.get_department()
    users = db.get_users()

    for key in skills:
        skill = skills[key]
        if skill.get("org_id") == organization_id:
            modified_skill = skill
            for user in users:
                current_user = users[user]
                if modified_skill.get("author_id") == current_user.get("id"):
                    modified_skill["author_name"] = current_user.get("name")
                    break
            for department in departments:
                current_department = departments[department]
                if modified_skill.get("dept_id") == current_department.get("id"):
                    modified_skill["dept_name"] = current_department.get("name")
                    break
            for skill_category in skill_categories:
                current_skill_category = skill_categories[skill_category]
                if modified_skill.get("category_id") == current_skill_category.get("id"):
                    modified_skill["category_name"] = current_skill_category.get("name")
                    break
            returned_skills.append(modified_skill)
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

#ORGANIZATION_MERMBERS

def get_organization_members():
    members = db.get_organization_members()
    return members


def create_organization_member(data):
    organization_member_data = data.model_dump()
    organization_member_id = str(uuid4())
    organization_member_data["id"] = organization_member_id

    db.create_organization_member(org_id=organization_member_data.get("org_id"),
                                  user_id=organization_member_data.get("user_id"),
                                  organization_member_id=organization_member_id)
    return organization_member_data

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