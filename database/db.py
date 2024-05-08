from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

from database.config import USER, PASSWORD, HOST, DB_PORT, DB_NAME

Base = declarative_base()

from database.Skills.utils import *
from database.Organizations.utils import *
from database.Departments.utils import *
from database.Users.utils import *
from database.Projects.utils import *
from database.Discussions.utils import *
from database.Messages.utils import *

engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{DB_PORT}/{DB_NAME}')


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

    # USERS==================================================================================================================

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
    def get_user(id):
        with session_scope() as session:
            return get_user(session=session, id=id)

    @staticmethod
    def get_organization_users(organization_id):
        returned_users = {}
        users = db.get_users()
        for user in users:
            current_user = users[user]
            current_user_id = current_user.get("org_id")
            if current_user_id == organization_id:
                returned_users[current_user.get("id")] = current_user
        return returned_users

    # SIGNUP_TOKENS
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

    # PASSWORD_RESET_TOKENS
    @staticmethod
    def create_password_reset_token(id, email, expires_at):
        with session_scope() as session:
            return create_password_reset_token(session=session,
                                               id=id,
                                               email=email,
                                               expires_at=expires_at)

    @staticmethod
    def get_password_reset_tokens():
        with session_scope() as session:
            return get_password_reset_tokens(session=session)

    @staticmethod
    def get_password_reset_token(id):
        with session_scope() as session:
            return get_password_reset_token(session=session, id=id)

    @staticmethod
    def delete_password_reset_token(id):
        with session_scope() as session:
            return delete_password_reset_tokens(session=session, id=id)

    @staticmethod
    def reset_password(user_id, password):
        with session_scope() as session:
            return reset_password(session=session, user_id=user_id, password=password)

    # ORGANIZATIONS==========================================================================================================

    @staticmethod
    def create_organization(name, hq_address, organization_id, created_at):
        with session_scope() as session:
            return create_organization(session=session,
                                       name=name,
                                       hq_address=hq_address,
                                       created_at=created_at,
                                       organization_id=organization_id)

    @staticmethod
    def create_organization_skill(skill_id, category_id, author_id, org_id, name, description, created_at):
        with session_scope() as session:
            return create_organization_skill(session=session,
                                             skill_id=skill_id,
                                             category_id=category_id,
                                             author_id=author_id,
                                             org_id=org_id,
                                             name=name,
                                             description=description,
                                             created_at=created_at)

    @staticmethod
    def delete_organization_skill(skill_id):
        with session_scope() as session:
            return delete_organization_skill(session=session, skill_id=skill_id)

    @staticmethod
    def update_organization_skill(category_id, name, skill_id, description, created_at):
        with session_scope() as session:
            return update_organization_skill(session=session,
                                             category_id=category_id,
                                             skill_id=skill_id,
                                             name=name,
                                             description=description,
                                             created_at=created_at)

    @staticmethod
    def get_organizations():
        with session_scope() as session:
            return get_organizations(session=session)

    @staticmethod
    def get_organizations_demo():
        with session_scope() as session:
            return get_organizations_demo(session=session)

    @staticmethod
    def get_organization(id):
        with session_scope() as session:
            return get_organization(session=session, id=id)

    @staticmethod
    def get_organization_info(id):
        with session_scope() as session:
            return get_organization_info(session=session, id=id)

    # USER ROLES
    @staticmethod
    def create_user_role(user_id, role_id):
        with session_scope() as session:
            return create_user_role(session=session, user_id=user_id, role_id=role_id)

    @staticmethod
    def user_roles_get(user_id):
        with session_scope() as session:
            user_roles = get_user_roles(session=session, user_id=user_id)
            returned_user_roles = {}
            for role in user_roles:
                if role.get("user_id") == user_id:
                    role_id = role.get("role_id")
                    role[role_id] = role
                    returned_user_roles[role_id] = user_id
            return returned_user_roles

    @staticmethod
    def get_org_user_roles(org_id):
        with session_scope() as session:
            all_user_roles = get_all_user_roles(session=session)
            org_user_roles = []
            users = db.get_organization_users(org_id)
            for role in all_user_roles:
                for user in users:
                    if user == role.get("user_id"):
                        org_user_roles.append(role)
            return org_user_roles

    @staticmethod
    def remove_user_role(user_id, role_id):
        with session_scope() as session:
            return remove_user_role(session=session, user_id=user_id, role_id=role_id)

    # ORGANIZATION_ROLES
    @staticmethod
    def create_organization_role(organization_role_id, name):
        with session_scope() as session:
            return create_organization_role(session=session, organization_role_id=organization_role_id, name=name)

    @staticmethod
    def get_organization_roles():
        with session_scope() as session:
            return get_organization_roles(session=session)

    # TEAM_ROLES


            # with session_scope() as session:
            # all_needed_roles = get_project_needed_roles(session=session)
            # needed_role_ids = []
            # for role_id in all_needed_roles:
            #     needed_role_ids.append(role_id)
            #
            # return needed_role_ids

    @staticmethod
    def get_all_organization_team_roles(org_id):
        with session_scope() as session:
            projects = db.get_org_projects(org_id)
            needed_role_ids = []

            for proj_id in projects:
                project_needed_roles, _ = db.get_project_needed_roles(proj_id, org_id)
                for needed_role in project_needed_roles:
                    needed_role_ids.append(needed_role.get("role_id"))

            return needed_role_ids

    @staticmethod
    def create_team_role(id, org_id, name):
        with session_scope() as session:
            return create_team_role(session=session,
                                    id=id,
                                    org_id=org_id,
                                    name=name)

    @staticmethod
    def update_team_role(id, name):
        with session_scope() as session:
            return update_team_role(session=session,
                                    id=id,
                                    name=name)

    @staticmethod
    def delete_team_role(id):
        with session_scope() as session:
            return delete_team_role(session=session, id=id)

    @staticmethod
    def get_team_roles(org_id):
        with session_scope() as session:
            return get_team_roles(session=session, org_id=org_id)

    # DEPARTMENTS============================================================================================================

    @staticmethod
    def create_department(name, org_id, department_id, created_at):
        with session_scope() as session:
            return create_department(session=session,
                                     org_id=org_id,
                                     name=name,
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

    @staticmethod
    def update_department(name, dept_id, manager_id):
        with session_scope() as session:
            return update_department(session=session,
                                     name=name,
                                     manager_id=manager_id,
                                     dept_id=dept_id)

    @staticmethod
    def delete_department(dept_id):
        with session_scope() as session:
            return delete_department(session=session,
                                     dept_id=dept_id)

    @staticmethod
    def remove_department_manager_id(dept_id, manager_id):
        with session_scope() as session:
            return remove_manager_id(session=session, dept_id=dept_id, manager_id=manager_id)

    @staticmethod
    def get_department_info(dept_id):
        with session_scope() as session:
            return get_department_info(session=session, dept_id=dept_id)

    # DEPARTMENT_MEMBERS
    @staticmethod
    def create_department_member(dept_id, user_id):
        with session_scope() as session:
            return create_department_member(session=session,
                                            dept_id=dept_id,
                                            user_id=user_id)

    @staticmethod
    def get_department_members(dept_id):
        with session_scope() as session:
            returned_members = []
            all_department_members = get_department_members(session=session)
            users = db.get_users()

            for member in all_department_members:
                member_dept_id = member.get("dept_id")
                member_user_id = member.get("user_id")

                if member_dept_id == dept_id:
                    member["name"] = users[member_user_id].get("name")
                    member["email"] = users[member_user_id].get("email")
                    returned_members.append(member)
            return returned_members

    @staticmethod
    def get_all_department_members():
        with session_scope() as session:
            all_department_members = get_department_members(session=session)
            return all_department_members

    @staticmethod
    def get_department_user(user_id):
        with session_scope() as session:
            all_department_members = get_department_members(session=session)
            for member in all_department_members:
                member_dept_id = member.get("dept_id")
                member_user_id = member.get("user_id")
                if str(member_user_id) == str(user_id):
                    return member_dept_id

    @staticmethod
    def delete_department_members(dept_id):
        with session_scope() as session:
            return delete_department_members(session=session, dept_id=dept_id)

    @staticmethod
    def delete_department_member(dept_id, user_id):
        with session_scope() as session:
            return delete_department_member(session=session, dept_id=dept_id, user_id=user_id)

    @staticmethod
    def get_department_manager_id():
        with session_scope() as session:
            org_roles = get_organization_roles(session=session)
            for role in org_roles:
                current_role = org_roles[role]
                if str(current_role.get("name")) == "dept_manager":
                    return role

    # SKILLS=================================================================================================================

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
            departments_skills = get_all_department_skills(session=session)
            for skill in skills:
                current_skill = skills[skill]
                if str(current_skill.get("org_id")) == str(organization_id):
                    current_skill_id = current_skill.get("id")
                    returned_skills[current_skill_id] = current_skill
                    returned_skills[current_skill_id]["dept_id"] = []
                    for departments_skill in departments_skills:
                        current_department_skill = departments_skills[departments_skill]
                        if str(current_skill_id) == str(current_department_skill.get("skill_id")):
                            dept_id = current_department_skill.get("dept_id")
                            returned_skills[current_skill_id]["dept_id"].append(dept_id)
            return returned_skills

    @staticmethod
    def get_skill(skill_id):
        with session_scope() as session:
            skill = get_skill(session=session, skill_id=skill_id)
            return skill

    # USER_SKILLS
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
    def get_user_skills(user_id):
        with session_scope() as session:
            all_user_skills = get_user_skills(session=session)
            returned_user_skills = []
            for user_skill in all_user_skills:
                if user_skill.get("user_id") == str(user_id):
                    returned_user_skills.append(user_skill)
            return returned_user_skills

    @staticmethod
    def get_users_skills():
        with session_scope() as session:
            users_skills = get_user_skills(session=session)
            return users_skills

    @staticmethod
    def get_org_user_skills(org_id):
        with session_scope() as session:
            returned_org_skills = []
            organization_skills = []

            org_skills = get_skills(session=session)
            for skill in org_skills:
                current_skill = org_skills[skill]
                if str(current_skill.get("org_id")) == str(org_id):
                    organization_skills.append(skill)
            users_skills = get_user_skills(session=session)
            for skill in users_skills:
                if skill.get("skill_id") in organization_skills:
                    returned_org_skills.append(skill)

            return returned_org_skills

    @staticmethod
    def update_user_skill(user_id, level, experience, skill_id):
        with session_scope() as session:
            return update_user_skill(session=session,
                                     user_id=user_id,
                                     skill_id=skill_id,
                                     level=level,
                                     experience=experience)

    @staticmethod
    def remove_user_skill(user_id, skill_id):
        with session_scope() as session:
            return remove_user_skill(session=session,
                                     user_id=user_id,
                                     skill_id=skill_id)

    @staticmethod
    def verify_user_skill(user_id, skill_id):
        with session_scope() as session:
            all_user_skills = get_user_skills(session)
            for user_skill in all_user_skills:
                if user_skill.get("user_id") == str(user_id) and user_skill.get("skill_id") == str(skill_id):
                    return True
        return False

    @staticmethod
    def get_skill_info(skill_id, org_id):
        with session_scope() as session:
            org_skill = get_skills(session)
            current_skill = org_skill[skill_id]
            if str(current_skill.get("org_id")) == str(org_id):
                return current_skill

    # SKILL ENDORSEMENTS

    @staticmethod
    def create_skill_endorsement(endo_id, org_id, skill_id, endo, description, proj_id, type, user_id):
        with session_scope() as session:
            return create_skill_endorsement(session=session,
                                            endo_id=endo_id,
                                            org_id=org_id,
                                            skill_id=skill_id,
                                            endo=endo,
                                            type=type,
                                            user_id=user_id,
                                            description=description,
                                            proj_id=proj_id)

    @staticmethod
    def get_skill_endorsements(skill_id, user_id):
        with session_scope() as session:
            returned_endorsements = []
            all_endorsements = get_endorsements(session=session)
            for endo in all_endorsements:
                if str(endo.get("skill_id")) == skill_id and str(endo.get("user_id")) == user_id:
                    returned_endorsements.append(endo)
            return returned_endorsements

    @staticmethod
    def get_user_endorsements(user_id):
        with session_scope() as session:
            returned_endorsements = []
            all_endorsements = get_endorsements(session=session)
            for endo in all_endorsements:
                if str(endo.get("user_id")) == user_id:
                    returned_endorsements.append(endo)
            return returned_endorsements

    @staticmethod
    def delete_skill_endorsement(user_id, skill_id, org_id):
        with session_scope() as session:
            return delete_single_skill_endorsement(session=session, user_id=user_id, org_id=org_id, skill_id=skill_id)
    # SKILL PROPOSALS

    @staticmethod
    def read_notification(proposal_id):
        with session_scope() as session:
            return read_notification(session=session, proposal_id=proposal_id)

    @staticmethod
    def propose_skill(skill_id, id, user_id, dept_id, level, experience, proposal, read, for_employee = None):
        with session_scope() as session:
            return propose_skill(session=session,
                                 id=id,
                                 dept_id=dept_id,
                                 user_id=user_id,
                                 skill_id=skill_id,
                                 level=level,
                                 read=read,
                                 experience=experience,
                                 for_employee=for_employee,
                                 proposal=proposal)

    @staticmethod
    def get_employee_skill_proposals(user_id):
        with session_scope() as session:
            proposed_skills = get_proposed_employee_skills(session=session, user_id=user_id)
            return proposed_skills

    @staticmethod
    def accept_employee_skill_proposal(proposal_id, level, experience):
        with session_scope() as session:
            return accept_employee_skill_proposal(session=session,
                                                  proposal_id=proposal_id,
                                                  level=level,
                                                  experience=experience)

    @staticmethod
    def delete_employee_skill_proposal(proposal_id):
        with session_scope() as session:
            return delete_employee_skill_proposal(session=session, proposal_id=proposal_id)

    @staticmethod
    def get_skill_proposals(department_id):
        with session_scope() as session:
            proposed_skills = []
            all_proposed_skills = get_proposed_skills(session=session)
            for skill in all_proposed_skills:
                current_skill = all_proposed_skills[skill]
                if str(current_skill.get("dept_id")) == str(department_id):
                    proposed_skills.append(all_proposed_skills[skill])
            return proposed_skills

    @staticmethod
    def delete_proposed_skill(user_id, skill_id):
        with session_scope() as session:
            return delete_proposed_skill(session=session, user_id=user_id, skill_id=skill_id)

    @staticmethod
    def create_project_assignment_proposal(id, assignment_id, read, user_id, role_ids, dept_id, proposal, comment = None, dealloc_reason = None, deallocated = None):
        with session_scope() as session:
            return create_project_assignment_proposal(session=session,
                                                      id=id,
                                                      assignment_id=assignment_id,
                                                      user_id=user_id,
                                                      role_ids=role_ids,
                                                      dept_id=dept_id,
                                                      comment=comment,
                                                      read=read,
                                                      proposal=proposal,
                                                      deallocated=deallocated,
                                                      dealloc_reason=dealloc_reason)

    @staticmethod
    def get_assignment_info(id):
        with session_scope() as session:
            return get_assignment_info(session=session, id=id)

    # SKILL_CATEGORIES
    @staticmethod
    def create_skill_category(name, org_id, created_at, skill_category_id):
        with session_scope() as session:
            return create_skill_category(session=session,
                                         name=name,
                                         org_id=org_id,
                                         created_at=created_at,
                                         skill_category_id=skill_category_id)

    @staticmethod
    def delete_skill_category(skill_category_id):
        with session_scope() as session:
            return delete_skill_category(session=session,
                                         skill_category_id=skill_category_id)

    @staticmethod
    def get_skill_categories(organization_id):
        with session_scope() as session:
            organization_skills = []

            skill_categories = get_skill_categories(session=session)

            for skill_category in skill_categories:
                current_category = skill_categories[skill_category]
                if current_category.get("org_id") == organization_id:
                    returned_body = {
                        "label": current_category.get("name"),
                        "value": current_category.get("id")
                    }
                    organization_skills.append(returned_body)

            return organization_skills

    @staticmethod
    def update_skill_category(id, org_id, name, modified_at):
        with session_scope() as session:
            return update_skill_category(session=session,
                                         id=id,
                                         org_id=org_id,
                                         name=name,
                                         modified_at=modified_at)

    # DEPARTMENT_SKILLS
    @staticmethod
    def create_department_skill(dept_id, skill_id, id):
        with session_scope() as session:
            return create_department_skill(session=session,
                                           dept_id=dept_id,
                                           skill_id=skill_id,
                                           id=id)

    @staticmethod
    def get_department_skills(dept_id):
        with session_scope() as session:
            department_skills = get_department_skills(session=session, dept_id=dept_id)
            returned_data = []
            for key in department_skills:
                returned_data.append(department_skills[key].get("skill_id"))
            return returned_data

    @staticmethod
    def get_all_department_skills():
        with session_scope() as session:
            return get_all_department_skills(session=session)

    @staticmethod
    def get_department_skill(skill_id, dept_id=None):
        with session_scope() as session:
            department_skills = get_all_department_skills(session=session)
            skill_departments = []
            for department in department_skills:
                current_department = department_skills[department]

                if dept_id:
                    if str(dept_id) == str(current_department.get("dept_id")) and str(skill_id) == str(
                            current_department.get("skill_id")):
                        skill_departments.append(department)
                elif current_department.get("skill_id") == str(skill_id):
                    skill_departments.append(department)

            return skill_departments

    @staticmethod
    def get_department_skills_names(organization_id):
        with session_scope() as session:
            dep_skills = get_all_department_skills(session=session)
            # GET ORGANIZATION DEPARTMENTS
            returned_departments = {}
            departments = get_department(session=session)
            for department in departments:
                current_department = departments[department]
                if str(current_department.get("org_id")) == str(organization_id):
                    current_department_id = current_department.get("id")
                    returned_departments[current_department_id] = current_department

            # Atribute name to each skill
            for dep_skill in dep_skills:
                current_dep_skill = dep_skills[dep_skill]
                for department in returned_departments:
                    current_department = returned_departments[department]
                    if current_dep_skill.get("dept_id") == current_department.get("id"):
                        current_dep_skill["dept_name"] = current_department.get("name")
            return dep_skills

    @staticmethod
    def skill_department_update(dept_id, skill_id, new_dept_id, new_skill_id):
        with session_scope() as session:
            return update_department_skill(session=session,
                                           dept_id=dept_id,
                                           skill_id=skill_id,
                                           new_dept_id=new_dept_id,
                                           new_skill_id=new_skill_id)

    @staticmethod
    def delete_department_skills(dept_id):
        with session_scope() as session:
            return delete_department_skills(session=session,
                                            dept_id=dept_id)

    @staticmethod
    def delete_department_skill(id):
        with session_scope() as session:
            return delete_department_skill(session=session, id=id)

    @staticmethod
    def get_department_statistics(dept_id, org_id):
        with session_scope() as session:
            department_skills = []
            returned_body = []

            # See how many members in department are
            department_members = db.get_department_members(dept_id)

            # Fetching department skills and user skills info from db and department members
            org_dept_skills = get_department_skills(session, dept_id)
            org_user_skills = db.get_org_user_skills(org_id)
            department_members = db.get_department_members(dept_id)
            # Search every skill from department
            for skill in org_dept_skills:
                current_skill = org_dept_skills[skill]
                department_skills.append(current_skill.get("skill_id"))
            # Search for every skill info
            for skill in department_skills:
                levels = [0, 0, 0, 0, 0, 0]
                total_users_skills = 0
                skill_info = db.get_skill_info(skill, org_id)

                # Search for every user with skills if it has a specific skill from department
                for user_skill in org_user_skills:
                    # Find if user is in department
                    is_in_department = False
                    for member in department_members:
                        if member.get("user_id") == user_skill.get("user_id"):
                            is_in_department = True
                    if str(user_skill.get("skill_id")) == str(skill) and is_in_department is True:
                        levels[0] = total_users_skills + 1
                        total_users_skills = total_users_skills + 1
                        current_user_skill_info = user_skill
                        current_user_skill_level = int(current_user_skill_info.get("level"))
                        levels[current_user_skill_level] = levels[current_user_skill_level] + 1
                returned_skill = {
                    "skill_name": skill_info.get("name"),
                    "levels": levels,
                    "total_department_members": len(department_members)
                }
                returned_body.append(returned_skill)
        return returned_body

    # PROJECTS===============================================================================================================
    @staticmethod
    def create_project(project_id, org_id, name, manager_id, period, start_date, deadline_date, status, description,
                       created_at, can_be_deleted, tech_stack):
        with session_scope() as session:
            return create_project(session=session,
                                  project_id=project_id,
                                  org_id=org_id,
                                  name=name,
                                  manager_id=manager_id,
                                  period=period,
                                  start_date=start_date,
                                  deadline_date=deadline_date,
                                  status=status,
                                  description=description,
                                  created_at=created_at,
                                  tech_stack=tech_stack,
                                  can_be_deleted=can_be_deleted)

    @staticmethod
    def get_org_projects(org_id):
        with session_scope() as session:
            returned_projects = []
            all_projects = get_projects(session)
            for project in all_projects:
                current_project = all_projects[project]
                if str(current_project.get("org_id")) == str(org_id):
                    returned_projects.append(project)
            return returned_projects

    @staticmethod
    def remove_project_manager_id(proj_id, manager_id):
        with session_scope() as session:
            return remove_project_manager_id(session=session, proj_id=proj_id, manager_id=manager_id)

    @staticmethod
    def get_project_info(proj_id):
        with session_scope() as session:
            return project_info(session=session, proj_id=proj_id)

    @staticmethod
    def get_manager_projects(user_id):
        with session_scope() as session:
            return get_manager_projects(session=session, user_id=user_id)

    @staticmethod
    def get_org_projects(org_id):
        with session_scope() as session:
            returned_projects = {}
            all_projects = get_projects(session=session)
            for project in all_projects:
                current_project = all_projects[project]
                if current_project.get("org_id") == org_id:
                    returned_projects[current_project.get("id")] = current_project
            return returned_projects

    @staticmethod
    def get_projects_id(proj_id):
        with session_scope() as session:
            returned_projects = []
            projects = get_projects(session=session)
            for project in projects:
                current_project = projects[project]
                if current_project.get("id") == proj_id:
                    returned_projects.append(current_project)
            return returned_projects

    @staticmethod
    def delete_project(project_id):
        with session_scope() as session:
            db.delete_project_required_skills(project_id)
            db.delete_project_needed_roles(project_id)
            delete_project(session=session, project_id=project_id)

    @staticmethod
    def update_project(name, period, start_date, deadline_date, status, description, project_id,
                       can_be_deleted, tech_stack):
        with session_scope() as session:
            return update_project(session=session,
                                  project_id=project_id,
                                  name=name,
                                  period=period,
                                  start_date=start_date,
                                  deadline_date=deadline_date,
                                  status=status,
                                  description=description,
                                  tech_stack=tech_stack,
                                  can_be_deleted=can_be_deleted)

    # PROJECT ASSIGNMENTS

    @staticmethod
    def create_project_assignment(project_assignments_id, proj_id, user_id, proposal, deallocated, dealloc_reason,
                                  work_hours, comment, org_id, role_ids):
        with session_scope() as session:
            return create_project_assignments(session=session,
                                              project_assignments_id=project_assignments_id,
                                              proj_id=proj_id,
                                              org_id=org_id,
                                              role_ids=role_ids,
                                              user_id=user_id,
                                              proposal=proposal,
                                              deallocated=deallocated,
                                              dealloc_reason=dealloc_reason,
                                              work_hours=work_hours,
                                              comment=comment)

    @staticmethod
    def update_project_assignment(assignment_id, role_ids = None, work_hours = None, comment = None, proposal = None, deallocated = None, dealloc_reason = None):
        with session_scope() as session:
            return update_project_assignments(session=session,
                                              assignment_id=assignment_id,
                                              role_ids=role_ids,
                                              work_hours=work_hours,
                                              comment=comment,
                                              proposal=proposal,
                                              deallocated=deallocated,
                                              dealloc_reason=dealloc_reason)

    @staticmethod
    def delete_project_assignment(assignment_id):
        with session_scope() as session:
            return delete_project_assignments(session=session,
                                              assignment_id=assignment_id)

    @staticmethod
    def delete_project_assignment_proposal(assignment_id):
        with session_scope() as session:
            return delete_project_assignment_proposal(session=session,
                                                      assignment_id=assignment_id)

    @staticmethod
    def accept_project_assignment(assignment_id):
        with session_scope() as session:
            return accept_project_assignment(session=session,
                                             assignment_id=assignment_id)

    @staticmethod
    def get_project_assignments(org_id):
        with session_scope() as session:
            return get_project_assignments(session=session, org_id=org_id)

    @staticmethod
    def get_project_approved_members(proj_id):
        with session_scope() as session:
            all_project_assigned_members = get_project_assigned_members(session=session, proj_id=proj_id)
            for member in all_project_assigned_members:
                if member.get("deallocated") == False and member.get("proposal") == False:
                    pass
                else:
                    all_project_assigned_members = [d for d in all_project_assigned_members if d != member]
            return all_project_assigned_members

    # USER TEAM ROLES

    @staticmethod
    def create_user_team_role(user_id, role_id, proposal):
        with session_scope() as session:
            return create_user_team_role(session=session,
                                         user_id=user_id,
                                         role_id=role_id)

    @staticmethod
    def get_user_team_roles():
        with session_scope() as session:
            return get_user_team_roles(session=session)

    # PROJECT TECH STACK SKILLS
    @staticmethod
    def create_project_tech_stack_skills(proj_id, skill_id, minimum_level):
        with session_scope() as session:
            return create_project_tech_stack_skill(session=session,
                                                   proj_id=proj_id,
                                                   skill_id=skill_id,
                                                   minimum_level=minimum_level)

    @staticmethod
    def get_project_tech_stack_skills(proj_id, org_id):
        with session_scope() as session:
            required_skills_list = []
            required_skills = get_project_tech_stack_skills(session=session)

            for key in required_skills:
                current_skill = required_skills[key]

                if str(current_skill.get("proj_id")) == str(proj_id):
                    current_skill.pop("proj_id", None)
                    current_skill["name"] = db.get_skill_info(current_skill.get("skill_id"), org_id).get("name")
                    required_skills_list.append(current_skill)

            return required_skills_list

    @staticmethod
    def update_project_tech_stack_skills(proj_id, skill_id, minimum_level):
        with session_scope() as session:
            return update_project_tech_stack_skill(session=session,
                                                   proj_id=proj_id,
                                                   skill_id=skill_id,
                                                   minimum_level=minimum_level)

    @staticmethod
    def delete_project_required_skills(project_id):
        with session_scope() as session:
            delete_required_skills(session=session, project_id=project_id)

    @staticmethod
    def delete_project_required_skill(proj_id, skill_id):
        with session_scope() as session:
            delete_required_skill(session=session, project_id=proj_id, skill_id=skill_id)

    # PROJECT NEEDED ROLES
    @staticmethod
    def create_project_needed_roles(id, proj_id, role_id, count):
        with session_scope() as session:
            return create_project_needed_role(session=session,
                                              id=id,
                                              proj_id=proj_id,
                                              role_id=role_id,
                                              count=count)

    @staticmethod
    def update_project_needed_role(id, count):
        with session_scope() as session:
            return update_project_needed_role(session=session,
                                              id=id,
                                              count=count)

    @staticmethod
    def get_project_needed_role(role_id, proj_id):
        with session_scope() as session:
            return get_project_needed_role(session=session, role_id=role_id, proj_id=proj_id)

    @staticmethod
    def get_project_needed_roles(proj_id, org_id):
        with session_scope() as session:
            all_needed_roles = get_project_needed_roles(session=session)
            returned_roles = []
            available_roles = []
            for role in all_needed_roles:
                current_role = all_needed_roles[role]
                if str(current_role.get("proj_id")) == str(proj_id):
                    role_id = current_role.get("role_id")
                    role_name = get_team_roles(session=session, org_id=org_id)[role_id].get("name")
                    current_role["role_name"] = role_name
                    if int(current_role.get("count")) > 0:
                        available_roles.append({"value": role_id, "label": role_name})
                    del current_role["proj_id"]
                    returned_roles.append(current_role)
            return returned_roles, available_roles

    @staticmethod
    def get_project_needed_roles_names(proj_id, org_id):
        with session_scope() as session:
            all_needed_roles = get_project_needed_roles(session=session)
            returned_roles = []
            for role in all_needed_roles:
                current_role = all_needed_roles[role]
                if str(current_role.get("proj_id")) == str(proj_id):
                    role_id = current_role.get("role_id")
                    role_name = get_team_roles(session=session, org_id=org_id)[role_id].get("name")
                    current_role["role_name"] = role_name
                    del current_role["role_id"], current_role["proj_id"]
                    returned_roles.append(current_role)
            return returned_roles

    @staticmethod
    def get_all_project_roles(proj_id, org_id):
        with session_scope() as session:
            all_needed_roles = get_project_needed_roles(session=session)
            returned_roles = []
            available_roles = []
            for role in all_needed_roles:
                current_role = all_needed_roles[role]
                if str(current_role.get("proj_id")) == str(proj_id):
                    role_id = current_role.get("role_id")
                    role_name = get_team_roles(session=session, org_id=org_id)[role_id].get("name")
                    current_role["role_name"] = role_name
                    if int(current_role.get("count")) > 0:
                        available_roles.append({"value": role_id, "label": role_name})
                    del current_role["proj_id"]
                    returned_roles.append(current_role)

            project_assignments = db.get_project_assignments(org_id)
            for assignment in project_assignments:
                if assignment.get("proj_id") == proj_id:
                    role_ids = assignment.get("role_ids")

                    for id in role_ids:
                        for role in returned_roles:
                            if role.get("role_id") == id:
                                role["count"] = int(role.get("count")) + 1

            return returned_roles, available_roles


    @staticmethod
    def delete_project_needed_roles(project_id):
        with session_scope() as session:
            delete_project_needed_roles(session=session, project_id=project_id)

    # PROJECT MEMBERS

    @staticmethod
    def create_project_member(proj_id, user_id):
        with session_scope() as session:
            return create_project_members(session=session,
                                          proj_id=proj_id,
                                          user_id=user_id)

    @staticmethod
    def get_project_members():
        with session_scope() as session:
            return get_project_members(session=session)

    # Payments

    @staticmethod
    def deactivate_account(organization_id):
        with session_scope() as session:
            return deactivate_account(session=session, organization_id=organization_id)

    @staticmethod
    def activate_account(organization_id):
        with session_scope() as session:
            return activate_account(session=session, organization_id=organization_id)

    # DISCUSSIONS ======================================================================================================

    @staticmethod
    def get_user_discussions(user_id):
        with session_scope() as session:
            return get_user_discussions(session=session, user_id=user_id)

    @staticmethod
    def get_discussions():
        with session_scope() as session:
            return get_discussions(session=session)

    @staticmethod
    def create_discussion(contacts, discussion_id, name):
        with session_scope() as session:
            return create_discussion(session=session, contacts=contacts, discussion_id=discussion_id, name=name)

    # CONTACTS ========================================================================================================
    @staticmethod
    def get_organization_contacts(organization_id):
        with session_scope() as session:
            return get_organization_contacts(session=session, organization_id=organization_id)

    # MESSAGES ========================================================================================================
    @staticmethod
    def create_message(message_id, user_id, value, discussion_id, created_at):
        with session_scope() as session:
            return create_message(session=session,
                                  id=message_id,
                                  user_id=user_id,
                                  value=value,
                                  discussion_id=discussion_id,
                                  created_at=created_at)

    @staticmethod
    def get_messages():
        with session_scope() as session:
            return get_messages(session)

    # PAYMENTS =========================================================================================================

    @staticmethod
    def update_organization_payment(id, status):
        with session_scope() as session:
            return update_organization_payment(session=session, id=id, status=status)

    @staticmethod
    def update_subscription(org_id):
        with session_scope() as session:
            return update_subscription(session=session, org_id=org_id)

    # CHAT GPT FEATURE==================================================================================================
    @staticmethod
    def get_all_details(org_id, user_id):
        with session_scope() as session:
            all_details = {
                'employee_assignments': get_project_assignments(session=session, org_id=org_id),
                'projects': db.get_org_projects(org_id=org_id),
                'team_roles': db.get_team_roles(org_id=org_id)
            }
        return all_details

db = DataBase()
