from typing import List

from fastapi import APIRouter, Depends, HTTPException
from Messages.models import *
from Messages.utils import *

auth_handler = AuthHandler()
message_router = APIRouter()


@message_router.post("/api/messages", response_model=List[MessageResponse])
async def create_message(message_data: Message, user_id: str = Depends(auth_handler.auth_wrapper)):
    discussion_id = message_data.discussion_id

    discussion, error = db.get_discussion(discussion_id)
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")

    discussion_contacts = discussion.get("contacts")
    if UUID(user_id) not in discussion_contacts:
        raise HTTPException(status_code=404, detail="The user is not part of the discussion")

    await create_new_message(message_data, user_id)

    messages, error = get_messages_by_discussion_id(user_id, discussion_id)
    if error:
        raise HTTPException(status_code=404, detail=error)

    return messages


@message_router.get("/api/messages", response_model=List[MessageResponse])
def get_messages(discussion_id: UUID, user_id: str = Depends(auth_handler.auth_wrapper)):
    discussion, error = db.get_discussion(discussion_id)
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")

    discussion_contacts = discussion.get("contacts")
    if UUID(user_id) not in discussion_contacts:
        raise HTTPException(status_code=404, detail="The user is not part of the discussion")

    messages, error = get_messages_by_discussion_id(user_id, discussion_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    else:
        return messages
