from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

from database.config import USER, PASSWORD, HOST, PORT, DB_NAME

Base = declarative_base()

from database.Skills.utils import *
from database.Organizations.utils import *
from database.Departments.utils import *
from database.Users.utils import *


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
    def create_admin(name, email, password, user_id, created_at, org_id):
        with session_scope() as session:
            return create_user(session=session,
                               name=name,
                               email=email,
                               password=password,
                               created_at=created_at,
                               org_id=org_id,
                               user_id=user_id)

    @staticmethod
    def create_employee(name, email, password, user_id, created_at, org_id):
        with session_scope() as session:
            return create_user(session=session,
                               name=name,
                               email=email,
                               password=password,
                               created_at=created_at,
                               org_id=org_id,
                               user_id=user_id)

    @staticmethod
    def get_users():
        with session_scope() as session:
            return get_users(session=session)

    @staticmethod
    def get_organization_users(user_id):
        returned_users = {}
        users = db.get_users()
        organization_id = users[user_id].get("org_id")
        for key in users:
            user = users[key]
            if user.get("org_id") == organization_id:
                returned_users[user.get("id")] = user
        return returned_users


    # ORGANIZATIONS
    @staticmethod
    def create_organization(name, hq_address, organization_id, created_at):
        with session_scope() as session:
            return create_organization(session=session,
                                       name=name,
                                       hq_address=hq_address,
                                       created_at=created_at,
                                       organization_id=organization_id)

    @staticmethod
    def get_organizations():
        with session_scope() as session:
            return get_organizations(session=session)


    @staticmethod
    def get_organization(id):
        with session_scope() as session:
            return get_organization(session=session, id=id)

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
    def get_department(organization_id):
        with session_scope() as session:
            returned_departments = {}

            departments = get_department(session=session)
            for department in departments:
                current_department = departments[department]
                if current_department.get("org_id") == organization_id:
                    current_department_id = current_department.get("id")
                    returned_departments[current_department_id] = current_department
            return returned_departments


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
    def get_user_roles(user_id):
        with session_scope() as session:
            return get_user_roles(session=session, user_id=user_id)


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
    def get_skills(organization_id):
        with session_scope() as session:
            returned_skills = {}
            skills = get_skills(session=session)
            for skill in skills:
                current_skill = skills[skill]
                if current_skill.get("org_id") == organization_id:
                    current_skill_id = current_skill.get("id")
                    returned_skills[current_skill_id] = current_skill
            return returned_skills


    # SKILL_CATEGORIES
    @staticmethod
    def create_skill_categories(name, org_id, created_at, skill_categories_id):
        with session_scope() as session:
            return create_skill_categories(session=session,
                                           name=name,
                                           org_id=org_id,
                                           created_at=created_at,
                                           skill_categories_id=skill_categories_id)

    @staticmethod
    def get_skill_categories(organization_id):
        with session_scope() as session:
            organization_skills = {}

            skill_categories = get_skill_categories(session=session)

            for skill_category in skill_categories:
                current_category = skill_categories[skill_category]
                if current_category.get("org_id") == organization_id:
                    current_category_id = current_category.get("id")
                    organization_skills[current_category_id] = current_category
            return organization_skills

    @staticmethod
    def update_skill_category(id, org_id, name, modified_at):
        with session_scope() as session:
            return update_skill_category(session=session,
                                         id=id,
                                         org_id=org_id,
                                         name=name,
                                         modified_at=modified_at)


    #DEPARTMENT_SKILLS
    @staticmethod
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
    @staticmethod
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


    #SIGNUP_TOKENS
    @staticmethod
    def create_signup_token(id, org_id, expires_at):
        with session_scope() as session:
            return create_signup_token(session=session,
                                       id=id,
                                       org_id=org_id,
                                       expires_at=expires_at)

    @staticmethod
    def delete_signup_token(id):
        with session_scope() as session:
            return delete_signup_token(session=session, id=id)

    @staticmethod
    def get_signup_tokens():
        with session_scope() as session:
            return get_signup_tokens(session=session)

    @staticmethod
    def get_org_signup_tokens(org_id):
        with session_scope() as session:
            return get_org_signup_tokens(session=session, org_id=org_id)

    @staticmethod
    def get_signup_token(id):
        with session_scope() as session:
            return get_signup_token(session=session, id=id)



    @staticmethod
    def get_all_details():
        with session_scope() as session:
            all_details = {}
            all_details['users'] = get_users(session=session)
            all_details['organizations'] = get_organizations(session=session)
            all_details['departments'] = get_department(session=session)
            all_details['department_members'] = get_department_members(session=session)
            all_details['user_roles'] = get_user_roles(session=session)

            return all_details


db = DataBase()
