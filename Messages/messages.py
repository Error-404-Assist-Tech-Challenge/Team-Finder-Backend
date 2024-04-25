from typing import List

from fastapi import APIRouter, Depends, HTTPException
from Messages.models import *
from Messages.utils import *

auth_handler = AuthHandler()
message_router = APIRouter()


@message_router.post("/api/messages", response_model=ResponseMessages)
async def create_message(message_data: Messages, user_id: str = Depends(auth_handler.auth_wrapper)):
    discussion_id = message_data.discussion_id

    discussion, error = db.get_discussions()
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found.")

    discussion = discussion.get(discussion_id)

    discussion_contacts = discussion.get("contacts", [])
    if user_id not in discussion_contacts:
        raise HTTPException(status_code=404, detail="The user is not part of the discussion")

    message_dict = create_new_message(message_data)
    message_dict["type"] = "message"
    return message_dict


@message_router.get("/api/messages", response_model=List[ResponseMessages])
def get_message(discussion_data: Discussions, user_id: str = Depends(auth_handler.auth_wrapper)):
    discussion_id = discussion_data.discussion_id
    discussion, error = db.get_discussions()
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found.")

    discussion = discussion.get(discussion_id)
    discussion_contacts = discussion.get("contacts", [])
    if user_id not in discussion_contacts:
        raise HTTPException(status_code=404, detail="The user is not part of the discussion")

    messages, error = get_messages_by_discussion_id(user_id, discussion_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    else:
        return messages
