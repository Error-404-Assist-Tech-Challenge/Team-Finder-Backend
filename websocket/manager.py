import os
from starlette.websockets import WebSocket

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

    async def connect(self, websocket: WebSocket, access_token):
        _, error = auth_handler.decode_token(access_token, auth_handler.access_secret, connect_websocket=True)
        self.active_connections[access_token] = websocket

        if error:
            self.active_connections.pop(access_token)
        else:
            await websocket.accept()

    async def disconnect(self, client_id):
        self.active_connections.pop(client_id)
