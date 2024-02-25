from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

from database.config import USER, PASSWORD, HOST, PORT, DB_NAME

Base = declarative_base()

# UTILS Import
from database.users.utils import *
from database.roles.utils import *
from database.user_roles.utils import *
from database.organizations.utils import *
from database.organization_members.utils import *
from database.departments.utils import *
from database.departments_member.utils import *

engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')


@contextmanager
def session_scope():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


Base.metadata.create_all(engine)


class DataBase:

    # USERS
    @staticmethod
    def create_users(name, email, password, user_id):
        with session_scope() as session:
            return create_user(session=session, name=name, email=email, password=password, user_id=user_id)

    @staticmethod
    def get_users():
        with session_scope() as session:
            return get_users(session=session)


    # ORGANIZATIONS
    @staticmethod
    def create_organization(name, admin_id, hq_address, organization_id):
        with session_scope() as session:
            return create_organization(session=session,
                                       admin_id=admin_id,
                                       name=name,
                                       hq_address=hq_address,
                                       organization_id=organization_id)

    @staticmethod
    def get_organizations():
        with session_scope() as session:
            return get_organizations(session=session)


    # ORGANIZATIONS_MEMBERS
    @staticmethod
    def create_organization_member(org_id, user_id, organization_member_id):
        with session_scope() as session:
            return create_organization_member(session=session, org_id=org_id, user_id=user_id, organization_member_id=organization_member_id)

    @staticmethod
    def get_organization_members():
        with session_scope() as session:
            return get_organization_members(session=session)


    # DEPARTMENTS
    @staticmethod
    def create_department(name, org_id, manager_id, department_id):
        with session_scope() as session:
            return create_department(session=session,
                                     org_id=org_id,
                                     name=name,
                                     manager_id=manager_id,
                                     department_id=department_id)

    @staticmethod
    def get_department():
        with session_scope() as session:
            return get_department(session=session)


    # DEPARTMENT_MEMBERS
    @staticmethod
    def create_department_member(dept_id, user_id, department_member_id):
        with session_scope() as session:
            return create_department_member(session=session,
                                            dept_id=dept_id,
                                            user_id=user_id,
                                            department_member_id=department_member_id)

    @staticmethod
    def get_department_members():
        with session_scope() as session:
            return get_department_members(session=session)


    # USER ROLES
    @staticmethod
    def create_user_role(user_id, role_id):
        with session_scope() as session:
            return create_user_role(session=session, user_id=user_id, role_id=role_id)

    @staticmethod
    def get_user_roles():
        with session_scope() as session:
            return get_user_roles(session=session)


    # PREDEFINED ROLES
    @staticmethod
    def get_roles():
        with session_scope() as session:
            return get_roles(session=session)

    @staticmethod
    def get_all_details():
        all_details = {}
        all_details['users'] = get_users(session=session)
        all_details['organizations'] = get_organizations(session=session)
        all_details['organization_members'] = get_organization_members(session=session)
        all_details['departments'] = get_department(session=session)
        all_details['department_members'] = get_department_members(session=session)
        all_details['user_roles'] = get_user_roles(session=session)
        all_details['roles'] = get_roles(session=session)

        return all_details


db = DataBase()
