from starlette.websockets import WebSocket, WebSocketDisconnect
from uuid import UUID

from auth import AuthHandler

auth_handler = AuthHandler()


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            return cls._instances[cls]
        cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConnectionManager(metaclass=SingletonMeta):
    def __init__(self):
        self.active_connections = {}

    async def broadcast_notification(self, user_id, notification):
        connection = None

        for token in self.active_connections:
            decoded_user_id, _ = auth_handler.decode_token(token, auth_handler.access_secret)

            if decoded_user_id == user_id:
                connection = self.active_connections.get(token)

        if connection:
            await connection.send_json(notification)

    async def broadcast_chat_messages(self, discussion_data, message_dict):
        connection = None
        contacts = discussion_data.get("contacts")
        discussion_id = discussion_data.get("id")

        for token in self.active_connections:
            decoded_user_id, _ = auth_handler.decode_token(token, auth_handler.access_secret)

            if UUID(decoded_user_id) in contacts:
                connection = self.active_connections.get(token)

            if connection:
                await connection.send_json(message_dict)

    async def connect(self, websocket: WebSocket, access_token):
        await websocket.accept()
        _, error = auth_handler.decode_token(access_token, auth_handler.access_secret, connect_websocket=True)
        self.active_connections[access_token] = websocket

        if error:
            raise WebSocketDisconnect(code=1008, reason="Expired or invalid access token")

    async def disconnect(self, access_token=None):
        self.active_connections.pop(access_token)
