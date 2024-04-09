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

    async def connect(self, websocket: WebSocket, access_token):
        await websocket.accept()
        self.active_connections[auth_handler.decode_token(access_token, os.environ["ACCESS_SECRET"])] = websocket

    async def disconnect(self, client_id):
        self.active_connections.pop(client_id)
