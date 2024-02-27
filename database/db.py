from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

from database.config import USER, PASSWORD, HOST, PORT, DB_NAME

Base = declarative_base()

from database.Skills.utils import *
from database.Organizations.utils import *
from database.Departments.utils import *
from database.users.utils import *


engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')


@contextmanager
def session_scope():
    Session = sessionmaker(bind=engine, expire_on_commit=False)
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
    def create_admin(name, email, password, user_id, created_at):
        with session_scope() as session:
            return create_user(session=session,
                               name=name,
                               email=email,
                               password=password,
                               created_at=created_at,
                               user_id=user_id)

    @staticmethod
    def get_users():
        with session_scope() as session:
            return get_users(session=session)

    @staticmethod
    def get_organization_users(organization_id):
        with session_scope() as session:
            returned_users = []
            users = db.get_users()
            organization_members = db.get_organization_members()
            for key in organization_members:
                organization_member = organization_members[key]
                if organization_member.get("org_id") == organization_id:
                    organization_member_id = organization_member.get("user_id")
                    for user in users:
                        current_user = users[user]
                        if current_user.get("id") == organization_member_id:
                            returned_users.append(current_user)
                            break

            return returned_users(session=session)


    # ORGANIZATIONS
    @staticmethod
    def create_organization(name, admin_id, hq_address, organization_id, created_at):
        with session_scope() as session:
            return create_organization(session=session,
                                       admin_id=admin_id,
                                       name=name,
                                       hq_address=hq_address,
                                       created_at=created_at,
                                       organization_id=organization_id)

    @staticmethod
    def get_organizations():
        with session_scope() as session:
            return get_organizations(session=session)

    # ORGANIZATIONS_MEMBERS
    @staticmethod
    def create_organization_member(org_id, user_id):
        with session_scope() as session:
            return create_organization_member(session=session, org_id=org_id, user_id=user_id)

    @staticmethod
    def get_organization_members():
        with session_scope() as session:
            return get_organization_members(session=session)

    #ORGANIZATION_ROLES
    @staticmethod
    def create_organization_role(id, name):
        with session_scope() as session:
            return create_organization_role(session=session, id=id, name=name)

    @staticmethod
    def get_organization_roles():
        with session_scope() as session:
            return get_organization_roles(session=session)

    # DEPARTMENTS
    @staticmethod
    def create_department(name, org_id, manager_id, department_id, created_at):
        with session_scope() as session:
            return create_department(session=session,
                                     org_id=org_id,
                                     name=name,
                                     manager_id=manager_id,
                                     created_at=created_at,
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


    # ROLES
    @staticmethod
    def create_roles(name, role_id):
        with session_scope() as session:
            return create_role(session=session, name=name, role_id=role_id)
    @staticmethod
    def get_roles():
        with session_scope() as session:
            return get_roles(session=session)

    #USER_SKILLS
    @staticmethod
    def create_user_skills(user_id, skill_id, level, experience, created_at):
        with session_scope() as session:
            return create_user_skills(session=session,
                                      user_id=user_id,
                                      skill_id=skill_id,
                                      level=level,
                                      created_at=created_at,
                                      experience=experience)

    @staticmethod
    def get_user_skills():
        with session_scope() as session:
            return get_user_skills(session=session)

    @staticmethod
    def update_user_skill(user_id, level, experience, skill_id):
        with session_scope() as session:
            return update_user_skill(session=session,
                                     user_id=user_id,
                                     skill_id=skill_id,
                                     level=level,
                                     experience=experience)

    #SKILLS
    @staticmethod
    def create_skill(category_id, name, description, created_at, skill_id, author_id, org_id):
        with session_scope() as session:
            return create_skill(session=session,
                                category_id=category_id,
                                name=name,
                                description=description,
                                created_at=created_at,
                                author_id=author_id,
                                org_id=org_id,
                                skill_id=skill_id)

    @staticmethod
    def get_skills():
        with session_scope() as session:
            return get_skills(session=session)

    # SKILL_CATEGORIES
    @staticmethod
    def create_skill_categories(name, dept_id, created_at, skill_categories_id):
        with session_scope() as session:
            return create_skill_categories(session=session,
                                           name=name,
                                           dept_id=dept_id,
                                           created_at=created_at,
                                           skill_categories_id=skill_categories_id)

    @staticmethod
    def get_skill_categories():
        with session_scope() as session:
            return get_skill_categories(session=session)



    #DEPARTMENT_SKILLS
    def create_department_skill(dept_id, skill_id):
        with session_scope() as session:
            return create_department_skill(session=session,
                                           dept_id=dept_id,
                                           skill_id=skill_id)

    @staticmethod
    def get_department_skills():
        with session_scope() as session:
            return get_department_skills(session=session)

    #TEAM_ROLES
    def create_team_role(id, org_id, name):
        with session_scope() as session:
            return create_team_role(session=session,
                                           id=id,
                                           org_id=org_id,
                                           name=name)

    @staticmethod
    def get_team_roles():
        with session_scope() as session:
            return get_team_roles(session=session)



    @staticmethod
    def get_all_details():
        with session_scope() as session:
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
