from fastapi import APIRouter, Depends, HTTPException
from Discussions.models import *
from Discussions.utils import *

auth_handler = AuthHandler()
discussions_router = APIRouter()


@discussions_router.post("/api/discussions")
def create_discussion(discussion_data: Discussions, user_id: str = Depends(auth_handler.auth_wrapper)):
    contacts = discussion_data.contacts
    users = db.get_users()
    for contact in contacts:
        if users.get(str(contact)) is None:
            raise HTTPException(status_code=404, detail="Contact not found.")

    contacts_discussions, error = get_contact_discussions(contacts)

    if error:
        raise HTTPException(status_code=404, detail=error)

    contacts_discussion = create_new_discussion(discussion_data)
    return contacts_discussion

# !!! Implement response model


@discussions_router.get("/api/discussions")
def get_discussion(user_id: str = Depends(auth_handler.auth_wrapper)):
    discussions, error = get_user_discussions(user_id)
    if error:
        raise HTTPException(status_code=500, detail="Failed to fetch discussions: " + error)
    else:
        return discussions
