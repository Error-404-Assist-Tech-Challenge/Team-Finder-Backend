from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from database.config import USER, PASSWORD, HOST, PORT, DB_NAME

Base = declarative_base()

# UTILS Import
from database.users.utils import *
from database.roles.utils import *
from database.user_roles.utils import *
from database.organizations.utils import *
from database.departments.utils import *


engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')

with engine.connect() as connection:
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)


class DataBase:

    # USERS
    @staticmethod
    def create_users(name, email, password, user_id):
        return create_user(session=session, name=name, email=email, password=password, user_id=user_id)

    @staticmethod
    def get_users():
        return get_users(session=session)


    # ORGANIZATIONS
    @staticmethod
    def create_organization(name, admin_id, hq_address, organization_id):
        return create_organization(session=session,
                                   admin_id=admin_id,
                                   name=name,
                                   hq_address=hq_address,
                                   organization_id=organization_id)

    @staticmethod
    def get_organizations():
        return get_organizations(session=session)


    # DEPARTMENTS
    @staticmethod
    def create_department(name, org_id, manager_id, department_id):
        return create_department(session=session,
                                 org_id=org_id,
                                 name=name,
                                 manager_id=manager_id,
                                 department_id=department_id)

    @staticmethod
    def get_department():
        return get_department(session=session)


    # USER ROLES
    @staticmethod
    def create_user_role(user_id, role_id):
        return create_user_role(session=session, user_id=user_id, role_id=role_id)

    @staticmethod
    def get_user_roles():
        return get_user_roles(session=session)


    # PREDEFINED ROLES
    @staticmethod
    def get_roles():
        return get_roles(session=session)


db = DataBase()