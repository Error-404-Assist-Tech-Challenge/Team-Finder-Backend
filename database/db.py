from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
Base = declarative_base()


from database.config import USER, PASSWORD, HOST, PORT, DB_NAME

# UTILS Import
from database.users.utils import *
from database.organization.utils import *
from database.departaments.utils import *


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

    @staticmethod
    def create_organization(name, admin_id, hq_address, organization_id):
        return create_organization(session, admin_id=admin_id, name=name, hq_address=hq_address, organization_id=organization_id)

    @staticmethod
    def get_organization(session=session):
        return get_organization(session)

    @staticmethod
    def create_departament(name, org_id, manager_id, departament_id):
        return create_departament(session, org_id=org_id, name=name, manager_id=manager_id,
                                   departament_id=departament_id)

    @staticmethod
    def get_departament(session=session):
        return get_departament(session)


db = DataBase()
