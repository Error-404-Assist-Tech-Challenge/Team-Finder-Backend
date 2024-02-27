from uuid import uuid4
from datetime import datetime
from passlib.context import CryptContext
from database.db import db

pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_users(organization_id):
    users = db.get_organization_users(organization_id)
    print(users)
    # users_roles = db.get_user_roles()
    # organization_roles = db.get_organization_roles()
    # for key in users:
    #     user = users[key]
    #
    # return users


def create_admin(data):
    user_data = data.model_dump()
    user_id = str(uuid4())
    user_data["id"] = user_id
    created_at = datetime.now()

    admin_obj, error = db.create_admin(name=user_data.get("name"),
                                       email=user_data.get("email"),
                                       password=get_password_hash(user_data.get("password")),
                                       created_at=created_at,
                                       user_id=user_id)

    if admin_obj:
        org_id = str(uuid4())
        db.create_organization(organization_id=org_id,
                               admin_id=user_id,
                               name=user_data.get("org_name"),
                               hq_address=user_data.get("hq_address"),
                               created_at=created_at)

        db.create_organization_member(org_id=org_id,
                                      user_id=user_id)

        admin_obj["org_id"] = org_id
    return admin_obj, error


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

            if verify_password(login_data.get("password"), user_data.get("password")):
                orgs_data = db.get_organization_members()
                login_data["id"] = user_data.get("id")
                login_data["name"] = user_data.get("name")

                if orgs_data.get(login_data.get("id")):
                    login_data["org_id"] = orgs_data.get(login_data.get("id")).get("org_id")

                    return login_data, False
                else:
                    return login_data, "Authorization complete but not apart of an organization"
            else:
                return login_data, "Incorrect password"

    return login_data, "Incorrect email"
