from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.config import USER, PASSWORD, HOST, PORT, DB_NAME
from database.models import Base
from database.utils import *

engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')

with engine.connect() as connection:
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)


class DataBase:
    @staticmethod
    def create_users(name, email, password, users_id):
        return create_user(session=session, name=name, email=email, password=password, users_id=users_id)

    @staticmethod
    def get_users():
        return get_users(session=session)

    def create_organization(name, email, password, users_id):
        return create_organization()

    @staticmethod
    def get_organization():
        return get_organization()


db = DataBase()
