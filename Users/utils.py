from uuid import uuid4
from auth import AuthHandler
from datetime import datetime
from passlib.context import CryptContext
from database.db import db

auth_handler = AuthHandler()
pwd_context = CryptContext(schemes=["bcrypt"])


def get_users(user_id):
    all_users = db.get_users()
    organization_id = all_users[user_id].get("org_id")
    users = db.get_organization_users(organization_id)
    users_roles = db.user_roles_get(user_id)
    organization_roles = db.get_organization_roles()
    for key in users:
        user = users[key]
        user["user_roles"] = []
        for user_role in users_roles:
            current_role_id = user_role
            current_role_user = users_roles[user_role]
            if current_role_user == user.get("id"):
                for organization_role in organization_roles:
                    current_organ_role = organization_roles[organization_role]
                    if current_organ_role.get("id") == current_role_id:
                        user["user_roles"].append(current_organ_role.get("name"))
    return users


def create_admin(data):
    user_data = data.model_dump()
    org_roles = db.get_organization_roles()
    user_id = str(uuid4())
    org_id = str(uuid4())
    user_data["id"] = user_id
    created_at = datetime.utcnow()
    hashed_password = auth_handler.get_password_hash(user_data.get("password"))
    db.create_organization(organization_id=org_id,
                           name=user_data.get("org_name"),
                           hq_address=user_data.get("hq_address"),
                           created_at=created_at)

    admin_obj, error = db.create_admin(name=user_data.get("name"),
                                       email=user_data.get("email"),
                                       password=hashed_password,
                                       created_at=created_at,
                                       org_id=org_id,
                                       user_id=user_id)

    for key in org_roles:
        if org_roles[key].get("name") == "admin":
            db.create_user_role(user_id=user_id, role_id=org_roles[key].get("id"))

    admin_obj["org_name"] = user_data.get("org_name")
    admin_obj["hq_address"] = user_data.get("hq_address")
    admin_obj["roles"] = ["admin"]

    return admin_obj, error


def create_employee(data):
    user_data = data.model_dump()
    user_id = str(uuid4())
    user_data["id"] = user_id
    created_at = datetime.utcnow()
    hashed_password = auth_handler.get_password_hash(user_data.get("password"))
    token = user_data.get("token")
    signup_token = db.get_signup_token(token)

    if signup_token:
        org_id = signup_token[token].get("org_id")
        format = "%Y-%m-%d %H:%M:%S"
        current_time = datetime.utcnow()

        if datetime.strptime(signup_token[token].get("expires_at"), format) > current_time:
            employee_obj, error = db.create_employee(name=user_data.get("name"),
                                                     email=user_data.get("email"),
                                                     password=hashed_password,
                                                     created_at=created_at,
                                                     org_id=org_id,
                                                     user_id=user_id)

            db.delete_signup_token(token)
        else:
            return False, "Sign up token expired"
    else:
        return False, "Sign up token invalid"

    org_data = db.get_organization(org_id)
    employee_obj["org_name"] = org_data.get("name")
    employee_obj["hq_address"] = org_data.get("hq_address")
    employee_obj["roles"] = ["employee"]

    return employee_obj, error


def account_exists(data):
    signup_data = data.model_dump()
    users_data = db.get_users()

    for key in users_data:
        if users_data[key].get("email") == signup_data.get("email"):
            return True
    return False


def login_user(data):
    login_data = data.model_dump()
    users_data = db.get_users()

    for key in users_data:
        if users_data[key].get("email") == login_data.get("email"):
            user_data = users_data[key]

            if auth_handler.verify_password(login_data.get("password"), user_data.get("password")):
                login_data["id"] = user_data.get("id")
                login_data["name"] = user_data.get("name")

                if user_data.get("org_id"):
                    org_data = db.get_organization(user_data.get("org_id"))
                    org_roles = db.get_organization_roles()
                    user_roles = db.user_roles_get(user_data.get("id"))

                    user_role_names = []
                    for role_id in user_roles:
                        if org_roles.get(role_id):
                            user_role_names.append(org_roles.get(role_id).get("name"))

                    if not user_role_names:
                        user_role_names.append("employee")

                    login_data["roles"] = user_role_names
                    login_data["org_id"] = user_data.get("org_id")
                    login_data["org_name"] = org_data.get("name")
                    login_data["hq_address"] = org_data.get("hq_address")
                    return login_data, False
                else:
                    return login_data, "Authentication successful but not apart of an organization"
            else:
                return login_data, "Incorrect password"

    return login_data, "Incorrect email"
