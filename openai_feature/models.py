from pydantic import BaseModel


class Chat_basemodel(BaseModel):
    system_message: str
    user_message: str
    chat_response: str
    details: str
    skills: str