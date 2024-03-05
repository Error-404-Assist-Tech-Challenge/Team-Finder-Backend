import os
import uuid
DB_NAME = os.environ["DB_NAME"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
HOST = os.environ["HOST"]
DB_PORT = os.environ["DB_PORT"]

zero_id = uuid.UUID(int=0)