from uuid import uuid4
from datetime import datetime, timedelta
import secrets
from database.db import db

department_manager_id = "fa124499-1762-4f3b-8a61-712307e1677a"

# USER_ROLES
def get_user_roles(user_id):
    user = db.get_user(user_id)
    organization_id = user.get("org_id")
    user_roles = db.get_org_user_roles(organization_id)
    return user_roles


def create_user_role(data):
    user_role_data = data.model_dump()
    db.create_user_role(user_id=user_role_data.get("user_id"),
                        role_id=user_role_data.get("role_id"))

    return user_role_data


def delete_user_role(data, admin_id):
    removed_data = data.model_dump()
    all_org_roles = db.get_organization_roles()
    for role in all_org_roles:
        current_role = all_org_roles[role]
        if removed_data.get("role_name") == current_role.get("name"):
            role_id = current_role.get("id")

            if current_role.get("name") == "admin":
                org_users = get_org_users(admin_id)
                admin_count = sum(1 for user in org_users if 'admin' in user['roles'])

                if admin_count == 1:
                    return None, "Deletion cannot proceed, the organization requires at least one administrator."

            db.remove_user_role(user_id=removed_data.get("user_id"),
                                role_id=role_id)

            # Check and remove if user_id is department manager
            departments = db.get_department(db.get_user(admin_id).get("org_id"))
            for department in departments:
                current_department = departments[department]
                if str(current_department.get("manager_id")) == str(removed_data.get("user_id")):
                    db.remove_manager_id(current_department.get("id"), None)
    returned_data = get_org_users(admin_id)
    return returned_data, None


# ORGANIZATION MEMBERS
def get_org_users(admin_id):
    admin = db.get_user(admin_id)
    org_id = admin.get("org_id")
    users = db.get_organization_users(org_id)
    org_roles = db.get_organization_roles()
    org_users = []

    for key in users:
        user = users[key]
        del user["password"], user["org_id"]

        if user.get("id") == admin_id:
            user["name"] = "You"

        user_roles = db.user_roles_get(user.get("id"))

        user_role_names = []
        for role_id in user_roles:
            if org_roles.get(role_id):
                user_role_names.append(org_roles.get(role_id).get("name"))

        user["roles"] = user_role_names
        org_users.append(user)

    def custom_sort(item):
        if item['name'] == 'You':
            return 'A'
        else:
            return item['name']

    sorted_data = sorted(org_users, key=custom_sort)

    return sorted_data


# ORGANIZATIONS
def get_organizations():
    organizations = db.get_organizations()
    return organizations


def get_unused_organization_skills(user_id):
    already_owned_skills = set()
    unused_skills = []

    users = db.get_users()
    organization_id = users[user_id].get("org_id")
    all_org_skills = db.get_skills(organization_id)
    user_skills = db.get_user_skills(user_id)
    for user_skill in user_skills:
        skill_id = user_skill.get("skill_id")
        already_owned_skills.add(skill_id)

    for skill_id, skill_info in all_org_skills.items():
        if skill_id not in already_owned_skills:
            unused_skills.append({"value": skill_id, "label": skill_info.get("name")})

    return unused_skills


def create_organization_skill(data, user_id):
    skill_data = data.model_dump()
    user_data = db.get_user(user_id)
    org_id = user_data.get("org_id")
    current_time = datetime.utcnow()

    db.create_organization_skill(category_id=skill_data.get("category_id"),
                                 author_id=user_id,
                                 org_id=org_id,
                                 name=skill_data.get("name"),
                                 description=skill_data.get("description"),
                                 created_at=current_time)

    returned_data = get_organizations_skills(user_id)

    return returned_data


def delete_organization_skill(data, user_id):
    skill_data = data.model_dump()
    db.delete_organization_skill(skill_data.get("id"))

    returned_data = get_organizations_skills(user_id)

    return returned_data


def update_organization_skill(data, user_id):
    modified_skill_data = data.model_dump()
    current_time = datetime.utcnow()
    db.update_organization_skill(category_id=modified_skill_data.get("category_id"),
                                 skill_id=modified_skill_data.get("skill_id"),
                                 name=modified_skill_data.get("name"),
                                 description=modified_skill_data.get("description"),
                                 created_at=current_time)

    returned_data = get_organizations_skills(user_id)

    return returned_data


def get_organizations_skills(user_id):
    returned_skills = []
    users = db.get_users()
    organization_id = users[user_id].get("org_id")
    skills = db.get_skills(organization_id)
    skill_categories = db.get_skill_categories(organization_id)

    for skill in skills:
        modified_skill = skills[skill]

        for user in users:
            current_user = users[user]
            if modified_skill.get("author_id") == current_user.get("id"):
                modified_skill["author_name"] = current_user.get("name")

        # Check if skill is authored
        if str(modified_skill.get("author_id")) == str(user_id):
            modified_skill["is_authored"] = True
        else:
            modified_skill["is_authored"] = False

        # Check if skill is in my department
        modified_skill["is_department_managed"] = False
        for department_id in modified_skill.get("dept_id"):
            department_info = db.get_department_info(department_id)

            if str(department_info.get("manager_id")) == modified_skill.get("author_id"):
                modified_skill["is_department_managed"] = True

        modified_skill["dept_name"] = []
        for department_id in modified_skill.get("dept_id"):
            department_info = db.get_department_info(department_id)
            modified_skill["dept_name"].append(department_info.get("name"))

        for skill_category in skill_categories:
            current_skill_category_id = skill_category.get("value")
            if modified_skill.get("category_id") == current_skill_category_id:
                modified_skill["category_name"] = skill_category.get("label")

        del modified_skill["org_id"], modified_skill["created_at"]
        returned_skills.append(modified_skill)
    sorted_data = sorted(returned_skills, key=lambda x: x['name'])
    return sorted_data


def create_organization(data):
    organization_data = data.model_dump()
    organization_id = str(uuid4())
    organization_data["id"] = organization_id
    db.create_dummy(name="DUMMY", email="email@gmail.com", password="12345", org_id=organization_id, created_at=organization_data.get("created_at"))
    db.create_organization(name=organization_data.get("name"),
                           hq_address=organization_data.get("hq_address"),
                           created_at=organization_data.get("created_at"),
                           organization_id=organization_id)

    return organization_data


# ORGANIZATION_ROLES
def get_organization_roles():
    user_roles = db.get_organization_roles()
    return user_roles


def create_organization_user_role(data, admin_id):
    role_data = data.model_dump()
    org_roles = db.get_organization_roles()
    user_roles = db.user_roles_get(str(role_data.get("user_id")))

    user_role_names = []
    for role_id in user_roles:
        if org_roles.get(role_id):
            user_role_names.append(org_roles.get(role_id).get("name"))

    for key in org_roles:
        if org_roles[key].get("name") == role_data.get("role_name"):
            if not user_roles.get(key):
                role_id = key
                user_role_names.append(org_roles[key].get("name"))
                db.create_user_role(user_id=role_data.get("user_id"), role_id=role_id)
            else:
                return None, f"User already has the {role_data.get('role_name')} role"

    returned_data = get_org_users(admin_id)
    return returned_data, None


# TEAM_ROLES
def get_team_roles(admin_id):
    user_data = db.get_user(admin_id)
    team_roles_data = db.get_team_roles(user_data.get("org_id"))

    for key in team_roles_data:
        team_roles_data[key].pop("org_id")

    team_roles = []
    for key, value in team_roles_data.items():
        team_roles.append({"id": key, "name": value["name"]})

    return team_roles


def create_team_role(data, admin_id):
    team_role_data = data.model_dump()
    user_data = db.get_user(admin_id)
    team_role_id = str(uuid4())
    db.create_team_role(id=team_role_id,
                        org_id=user_data.get("org_id"),
                        name=team_role_data.get("name"))

    returned_data = get_team_roles(admin_id)

    return returned_data


def update_team_role(data, admin_id):
    team_role_data = data.model_dump()
    db.update_team_role(id=team_role_data.get("id"),
                        name=team_role_data.get("name"))

    returned_data = get_team_roles(admin_id)

    return returned_data


def delete_team_role(data, admin_id):
    team_role_data = data.model_dump()
    response, error = db.delete_team_role(id=team_role_data.get("id"))

    returned_data = get_team_roles(admin_id)

    return returned_data, error


# SIGNUP_TOKENS
def create_signup_token(user_id):
    user_data = db.get_user(user_id)
    format = "%Y-%m-%d %H:%M:%S"
    current_time = datetime.utcnow().strftime(format)
    expires_at = datetime.strptime(current_time, format) + timedelta(hours=12)
    id = secrets.token_urlsafe(16)

    token, error = db.create_signup_token(id, user_data.get("org_id"), expires_at)

    return token, error


def get_organization_signup_tokens(user_id):
    user_data = db.get_user(user_id)
    tokens = db.get_org_signup_tokens(user_data.get("org_id"))
    tokens = [{k: v for k, v in token.items() if k != 'org_id'} for token in tokens]
    return tokens


def verify_signup_token(id):
    tokens = db.get_signup_tokens()
    format = "%Y-%m-%d %H:%M:%S"
    current_time = datetime.utcnow()

    for token in tokens:
        token_expiry = datetime.strptime(token["expires_at"], format)
        if token.get("id") == id:
            if token_expiry > current_time:
                org_data = db.get_organization(token.get("org_id"))
                token["org_name"] = org_data.get("name")
                token["hq_address"] = org_data.get("hq_address")
                del token["org_id"]
                del token["expires_at"]
                return token, None
            else:
                return None, "Expired token"
    return None, "Invalid token"
