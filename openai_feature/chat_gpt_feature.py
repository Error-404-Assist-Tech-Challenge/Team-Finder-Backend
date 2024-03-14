from fastapi import APIRouter, Depends

from auth import AuthHandler
from openai_feature.models import *
from openai_feature.utils import *

chat_gpt_router = APIRouter()
auth_handler = AuthHandler()

user_id = "34d00903-475a-4c10-9fa7-64b0b9def259"


@chat_gpt_router.post("/api/chat_gpt_feature")
def create_chat_gpt_response_route(chat_gpt_data: Chat_basemodel):
    return make_chat_gpt_request(chat_gpt_data, user_id)
