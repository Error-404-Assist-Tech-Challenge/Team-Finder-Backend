from fastapi import APIRouter
from openai_feature.models import Chat_basemodel
from openai_feature.utils import *

chat_gpt_router = APIRouter()

@chat_gpt_router.post("/api/chat_gpt_feature", response_model=Chat_basemodel)
def create_chat_gpt_response_route(chat_gpt_data: Chat_basemodel):
    return make_chat_gpt_request(chat_gpt_data)
