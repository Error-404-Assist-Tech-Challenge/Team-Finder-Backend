from uuid import uuid4, UUID
from auth import AuthHandler
from passlib.context import CryptContext
from database.db import db

auth_handler = AuthHandler()
pwd_context = CryptContext(schemes=["bcrypt"])


def get_user_discussions(user_id):
    user_discussions, error = db.get_user_discussions(user_id)
    if user_discussions:
        for discussion in user_discussions:

            if not discussion.get("name"):
                # Getting the discussion name
                if len(discussion.get("contacts")) == 1:
                    user_data = db.get_user(discussion.get("contacts")[0])
                    discussion["name"] = user_data.get("name")
                else:
                    for contact_id in discussion.get("contacts"):
                        if contact_id != user_id:
                            user_data = db.get_user(discussion.get("contacts")[0])
                            discussion["name"] = user_data.get("name")
                            break

            # Getting the names of all contacts
            contacts = []
            for contact_id in discussion.get("contacts"):
                user_data = db.get_user(contact_id)
                contacts.append({"id": contact_id, "name": user_data.get("name")})
            discussion["contacts"] = contacts

        return user_discussions, None
    else:
        return None, "No discussions found for this user"


def create_new_discussion(data):
    discussion_id = str(uuid4())
    discussion_data = data.model_dump()
    contacts = list(set(discussion_data.get("contacts")))

    db.create_discussion(contacts=contacts, discussion_id=discussion_id,
                         name=discussion_data.get("name"))

    return data


def get_contact_discussions(contacts):
    discussions, _ = db.get_discussions()

    for discussion in discussions:
        contact_ids = [UUID(uuid) for uuid in discussion.get("contacts")]

        if sorted(contact_ids) == sorted(contacts):
            return "Discussion already exists"

    return None