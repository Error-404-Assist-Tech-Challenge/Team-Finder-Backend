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

#USERS==================================================================================================================

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


#ORGANIZATIONS==========================================================================================================

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
    def get_organization(id):
        with session_scope() as session:
            return get_organization(session=session, id=id)


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

    #ORGANIZATION_ROLES
    @staticmethod
    def create_organization_role(organization_role_id, name):
        with session_scope() as session:
            return create_organization_role(session=session, organization_role_id=organization_role_id, name=name)

    @staticmethod
    def get_organization_roles():
        with session_scope() as session:
            return get_organization_roles(session=session)

    #TEAM_ROLES
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


#DEPARTMENTS============================================================================================================

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
    def remove_manager_id(dept_id, manager_id):
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
            departments_skills = get_department_skills(session=session)
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

    # SKILL PROPOSALS

    @staticmethod
    def propose_skill(skill_id, user_id, dept_id, level, experience):
        with session_scope() as session:
            return propose_skill(session=session,
                                 dept_id=dept_id,
                                 user_id=user_id,
                                 skill_id=skill_id,
                                 level=level,
                                 experience=experience)

    @staticmethod
    def get_skill_proposals():
        with session_scope() as session:
            return get_proposed_skills(session=session)

    @staticmethod
    def delete_proposed_skill(user_id, skill_id):
        with session_scope() as session:
            return delete_proposed_skill(session=session, user_id=user_id, skill_id=skill_id)


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
    def get_department_skills():
        with session_scope() as session:
            return get_department_skills(session=session)

    @staticmethod
    def get_department_skill(skill_id, dept_id = None):
        with session_scope() as session:
            department_skills = get_department_skills(session=session)
            skill_departments = []
            for department in department_skills:
                current_department = department_skills[department]

                if dept_id:
                    if str(dept_id) == str(current_department.get("dept_id")) and str(skill_id) == str(current_department.get("skill_id")):
                        skill_departments.append(department)
                elif current_department.get("skill_id") == str(skill_id):
                    skill_departments.append(department)

            return skill_departments

    @staticmethod
    def get_department_skills_names(organization_id):
        with session_scope() as session:
            dep_skills = get_department_skills(session=session)
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
            reference_user_skill = {}

            org_dept_skills = get_department_skills(session)
            org_user_skills = get_user_skills(session)
            # Modifying user_skills for reference search
            for user_skill in org_user_skills:
                # Verifying if user is in organization
                current_user_id = user_skill.get("user_id")
                if db.get_user(current_user_id).get("org_id") == org_id:
                    reference_user_skill[user_skill.get("user_id")] = {
                        "skill_id": user_skill.get("skill_id"),
                        "level": user_skill.get("level"),
                        "experience": user_skill.get("experience")
                    }

            # Search every skill from department
            for skill in org_dept_skills:
                current_skill = org_dept_skills[skill]
                if str(current_skill.get("dept_id")) == str(dept_id):
                    department_skills.append(current_skill.get("skill_id"))
            # Search for every skill info
            for skill in department_skills:
                levels = [0, 0, 0, 0, 0, 0]
                total_users_skills = 0
                skill_info = db.get_skill_info(skill, org_id)

                # Search for every user with skills if has a specific skill
                for user_skill in reference_user_skill:
                    if str(reference_user_skill[user_skill].get("skill_id")) == str(skill):
                        levels[0] = total_users_skills + 1
                        total_users_skills = total_users_skills + 1
                        current_user_skill_info = reference_user_skill[user_skill]
                        current_user_skill_level = int(current_user_skill_info.get("level"))
                        levels[current_user_skill_level] = levels[current_user_skill_level]+1
                returned_skill = {
                    "skill_name": skill_info.get("name"),
                    "levels": levels
                }
                returned_body.append(returned_skill)
        return returned_body

#PROJECTS===============================================================================================================
    @staticmethod
    def create_project(project_id, org_id, name, manager_id, period, start_date, deadline_date, status, description, created_at):
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
                                  created_at=created_at)

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

    # PROJECT ASSIGNMENTS
    @staticmethod
    def create_project_assignment(project_assignments_id, proj_id, user_id, proj_manager_id, proposal, deallocated, dealloc_reason, work_hours, comment):
        with session_scope() as session:
            return create_project_assignments(session=session,
                                              project_assignments_id=project_assignments_id,
                                              proj_id=proj_id,
                                              user_id=user_id,
                                              proj_manager_id=proj_manager_id,
                                              proposal=proposal,
                                              deallocated=deallocated,
                                              dealloc_reason=dealloc_reason,
                                              work_hours=work_hours,
                                              comment=comment)

    @staticmethod
    def get_project_assignments():
        with session_scope() as session:
            return get_project_assignments(session=session)

    #USER TEAM ROLES
    @staticmethod
    def create_user_team_role(user_id, role_id, proposal):
        with session_scope() as session:
            return create_user_team_role(session=session,
                                          user_id=user_id,
                                          role_id=role_id,
                                          proposal=proposal)


    @staticmethod
    def get_user_team_roles():
        with session_scope() as session:
            return get_user_team_roles(session=session)

    #PROJECT TECH STACK SKILLS
    @staticmethod
    def create_project_tech_stack_skills(proj_id, tech_stack):
        with session_scope() as session:
            return create_project_tech_stack_skill(session=session,
                                                   proj_id=proj_id,
                                                   tech_stack=tech_stack)


    @staticmethod
    def get_project_tech_stack_skills():
        with session_scope() as session:
            return get_project_tech_stack_skills(session=session)

    #PROJECT NEEDED ROLES
    @staticmethod
    def create_project_needed_roles(id, proj_id, role_id, count):
        with session_scope() as session:
            return create_project_needed_role(session=session,
                                              id=id,
                                              proj_id=proj_id,
                                              role_id=role_id,
                                              count=count)
    @staticmethod
    def get_project_needed_roles():
        with session_scope() as session:
            return get_project_needed_roles(session=session)

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

#CHAT GPT FEATURE=======================================================================================================
    @staticmethod
    def get_all_details():
        with session_scope() as session:
            all_details = {}
            all_details['Users'] = get_users(session=session)
            all_details['organizations'] = get_organizations(session=session)
            all_details['departments'] = get_department(session=session)
            all_details['department_members'] = get_department_members(session=session)
            all_details['user_roles'] = get_user_roles(session=session)
            #Plus the rest of the database
            return all_details


db = DataBase()
