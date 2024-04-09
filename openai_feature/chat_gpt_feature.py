from fastapi import APIRouter, Depends

from auth import AuthHandler
from openai_feature.models import *
from openai_feature.utils import *

chat_gpt_router = APIRouter(tags=["CHAT GPT"])
auth_handler = AuthHandler()


@chat_gpt_router.post("/api/chat_gpt_feature", response_model=List[Chat_Response])
def create_chat_gpt_response_route(chat_gpt_data: Chat_basemodel, user_id: str = Depends(auth_handler.auth_wrapper)):
    return make_chat_gpt_request(chat_gpt_data, user_id)
