from collections import Counter
from uuid import uuid4
from auth import AuthHandler
from datetime import datetime
from passlib.context import CryptContext
from database.db import db

auth_handler = AuthHandler()
pwd_context = CryptContext(schemes=["bcrypt"])


def get_user_discussions(user_id):
    user_discussions = db.get_user_discussions(user_id)
    if user_discussions:
        return user_discussions, None
    else:
        return None, "No discussions found for this user"


def create_new_discussion(data):
    discussion_id = str(uuid4())
    discussion_data = data.model_dump()
    discussion_data["id"] = discussion_id

    db.create_discussion(contacts=discussion_data["contacts"], discussion_id=discussion_data["id"],
                         name=discussion_data["name"])

    return discussion_data


def get_contact_discussions(data):
    discussions, error = db.get_discussions()
    if discussions:
        for discussion in discussions:
            contact_id = discussion.get("contacts")
            if Counter(contact_id) == Counter(data):
                return discussion, None
    return None, None
