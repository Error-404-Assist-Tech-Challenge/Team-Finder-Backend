from uuid import uuid4
from auth import AuthHandler
from datetime import datetime
from passlib.context import CryptContext
from database.db import db
from websocket.manager import ConnectionManager

auth_handler = AuthHandler()
connection_manager = ConnectionManager()
pwd_context = CryptContext(schemes=["bcrypt"])


async def create_new_message(message_data, user_id):
    messages, error = db.get_messages()
    message_dict = message_data.model_dump()
    message_id = str(uuid4())

    time = datetime.now()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    message_dict["id"] = message_id
    messages[message_id] = message_dict
    message_dict["created_at"] = formatted_time
    message_dict["discussion_id"] = str(message_dict.get("discussion_id"))

    message = db.create_message(
        message_id=message_dict["id"],
        discussion_id=message_dict["discussion_id"],
        user_id=user_id,
        value=message_dict["value"],
        created_at=message_dict["created_at"])


    if message:
        discussion_data, error = db.get_discussion(message_dict["discussion_id"])
        await connection_manager.broadcast_chat_messages(discussion_data, message_dict)

    return message


def get_messages_by_discussion_id(my_user_id, discussion_id):
    messages, error = db.get_messages()
    users_dict = db.get_users()
    message_list = []

    if messages:
        for key in messages:
            message = messages[key]
            if message.get("discussion_id") == str(discussion_id):
                user_id = message.get("user_id")
                if user_id == my_user_id:
                    message["name"] = "You"
                else:
                    message["name"] = users_dict.get(user_id, {}).get("name")
                message_list.append(message)

        return message_list, None
    else:
        return [], "No messages found"
