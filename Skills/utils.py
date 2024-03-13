from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException

from database.db import db

from Organizations.utils import get_organizations_skills


# SKILLS


def get_skills(user_id):
    users = db.get_users()
    organization_id = users[user_id]
    skills = db.get_skills(organization_id)
    return skills


def create_skills(data):
    skill_data = data.model_dump()
    skill_id = str(uuid4())
    skill_data["id"] = skill_id

    db.create_skill(name=skill_data.get("name"),
                    description=skill_data.get("description"),
                    category_id=skill_data.get("category_id"),
                    created_at=skill_data.get("created_at"),
                    author_id=skill_data.get("author_id"),
                    org_id=skill_data.get("org_id"),
                    skill_id=skill_id)

    return skill_data


# USER_SKILLS
def get_skills_by_users_id(user_id):
    organization_id = db.get_user(user_id).get("org_id")
    user_skills = db.get_user_skills(user_id)
    skills = db.get_skills(organization_id)
    skill_categories = get_skill_categories(user_id)
    user_skills_list = []

    for user_skill in user_skills:
        if user_skill.get("user_id") == user_id:
            user_skill_id = user_skill.get("skill_id")
            if user_skill_id in skills:
                skill = skills[user_skill_id]

                # Put skill category in user skills
                for skill_category in skill_categories:
                    if skill_category.get("value") == skill.get("category_id"):
                        user_skill["category_name"] = skill_category.get("label")
                # Put name in user skills
                skill_name = skill.get("name")
                user_skill["skill_name"] = skill_name
                # Put description in user skills
                skill_description = skill.get("description")
                user_skill["skill_description"] = skill_description

                # Put author in user skills
                skill_author = skill.get("author_id")
                user_skill["skill_author"] = db.get_user(skill_author).get("name")

                # Put skill endorsements
                user_skill["skill_endorsements"] = db.get_skill_endorsements(skill.get("id"))
                user_skills_list.append(user_skill)
    user_skills_list.sort(key=lambda x: x.get("skill_name", "").lower())
    return user_skills_list


def create_user_skills(data, user_id):
    user_skill_data = data.model_dump()
    is_manager = False

    # Check if user added an endorsement to his skill
    endorsements = user_skill_data.get("endorsements")
    if endorsements is not None:
        organization_id = db.get_user(user_id).get("org_id")
        for endo in endorsements:
            endo_id = str(uuid4())
            proj_id = endo.get("proj_id")

            # Check if project has or not project id
            if proj_id == '':
                db.create_skill_endorsement(endo_id=endo_id,
                                            org_id=organization_id,
                                            skill_id=user_skill_data.get("skill_id"),
                                            endo=endo.get("endorsement"),
                                            description=endo.get("description"),
                                            proj_id=None,
                                            type=endo.get("type"))
            else:
                db.create_skill_endorsement(endo_id=endo_id,
                                            org_id=organization_id,
                                            skill_id=user_skill_data.get("skill_id"),
                                            endo=endo.get("endorsement"),
                                            description=endo.get("description"),
                                            proj_id=endo.get("proj_id"),
                                            type=endo.get("type"))

    # Logic skill proposal
    skill_id = user_skill_data.get("skill_id")

    # Search if user exists in a department
    department_id = db.get_department_user(user_id)
    # Search if user is manager to a department
    if not department_id:
        departments = db.get_department(db.get_user(user_id).get("org_id"))
        for department in departments:
            current_department = departments[department]
            if str(current_department.get("manager_id")) == str(user_id):
                department_id = current_department.get("id")
                is_manager = True
    # If user is not a manager and has a department user can propose skill
    if department_id and not is_manager:
        propose_skill = str(uuid4())
        db.propose_skill(id=propose_skill,
                         skill_id=skill_id,
                         user_id=user_id,
                         dept_id=department_id,
                         level=user_skill_data.get("level"),
                         experience=user_skill_data.get("experience"),
                         read=False,
                         proposal=False)
        return get_skills_by_users_id(user_id)
    # If user is manager auto accept is implemented
    elif is_manager:
        # Verify if manager has or not having that skill
        manager_skills = db.get_user_skills(user_id)
        skill_found = False
        for skill in manager_skills:
            if str(skill.get("skill_id")) == str(skill_id):
                skill_found = True
        if skill_found:
            db.update_user_skill(skill_id=skill_id,
                                 user_id=user_id,
                                 level=user_skill_data.get("level"),
                                 experience=user_skill_data.get("experience"))
            return get_skills_by_users_id(user_id=user_id)
        else:
            db.create_user_skills(skill_id=skill_id,
                                  user_id=user_id,
                                  level=user_skill_data.get("level"),
                                  experience=user_skill_data.get("experience"),
                                  created_at=datetime.now().isoformat())
            return get_skills_by_users_id(user_id=user_id)
    # If user doesn't have a skill he cannot propose to anybody therefore we throw error 409
    else:
        raise HTTPException(status_code=409, detail="Department not found for the user")


def get_department_notifications(user_id):
    dep_skill_proposals = get_skill_proposals(user_id)
    returned_notifications = []
    for proposal in dep_skill_proposals:
        if str(proposal.get("read")) == "False":
            role_id = proposal.get("role_id")
            skill_id = proposal.get("skill_id")
            if str(skill_id) != "None":
                returned_body = {
                    "skill_id": skill_id,
                    "user_name": proposal.get("user_name"),
                    "skill_name": proposal.get("skill_name")
                }
                returned_notifications.append(returned_body)
            else:
                returned_body = {
                    "role_id": role_id,
                    "project_name": proposal.get("project_name")
                }
                returned_notifications.append(returned_body)
    return returned_notifications


def remove_user_skill(data, user_id):
    skill_data = data.model_dump()
    db.remove_user_skill(user_id=user_id,
                         skill_id=skill_data.get("skill_id"))
    db.delete_user_endorsements(skill_id=skill_data.get("skill_id"), org_id=db.get_user(user_id).get("org_id"))
    returned_data = get_skills_by_users_id(user_id)

    return returned_data


def update_user_skills(data, user_id):
    user_skill_data = data.model_dump()
    is_manager = False
    skill_id = user_skill_data.get("skill_id")
    # Search if user exists in a department
    department_id = db.get_department_user(user_id)
    # Search if user is manager to a department
    if not department_id:
        departments = db.get_department(db.get_user(user_id).get("org_id"))
        for department in departments:
            current_department = departments[department]
            if str(current_department.get("manager_id")) == str(user_id):
                department_id = current_department.get("id")
                is_manager = True

    if department_id and not is_manager:

        # Update endorsements
        endorsements = user_skill_data.get("endorsements")
        if endorsements is not None:
            db.delete_user_endorsements(skill_id=skill_id, org_id=db.get_user(user_id).get("org_id"))
            for endo in endorsements:
                proj_id = endo.get("proj_id")
                if proj_id == '':
                    db.create_skill_endorsement(endo_id=str(uuid4()),
                                                org_id=db.get_user(user_id).get("org_id"),
                                                skill_id=user_skill_data.get("skill_id"),
                                                endo=endo.get("endorsement"),
                                                description=endo.get("description"),
                                                proj_id=None,
                                                type=endo.get("type"))
                else:
                    db.create_skill_endorsement(endo_id=str(uuid4()),
                                                org_id=db.get_user(user_id).get("org_id"),
                                                skill_id=user_skill_data.get("skill_id"),
                                                endo=endo.get("endorsement"),
                                                description=endo.get("description"),
                                                proj_id=endo.get("proj_id"),
                                                type=endo.get("type"))
        else:
            db.delete_user_endorsements(skill_id=skill_id, org_id=db.get_user(user_id).get("org_id"))
        db.propose_skill(id=str(uuid4()),
                         proposal=False,
                         skill_id=skill_id,
                         user_id=user_id,
                         dept_id=department_id,
                         level=user_skill_data.get("level"),
                         experience=user_skill_data.get("experience"),
                         read=False)
        returned_data = get_skills_by_users_id(user_id)
        return returned_data
    elif is_manager:
        # Update user skill
        db.update_user_skill(skill_id=skill_id,
                             user_id=user_id,
                             level=user_skill_data.get("level"),
                             experience=user_skill_data.get("experience"))
        # Update endorsements
        endorsements = user_skill_data.get("endorsements")
        if endorsements is not None:
            db.delete_user_endorsements(skill_id=skill_id, org_id=db.get_user(user_id).get("org_id"))
            for endo in endorsements:
                proj_id = endo.get("proj_id")
                if proj_id == '':
                    db.create_skill_endorsement(endo_id=str(uuid4()),
                                                org_id=db.get_user(user_id).get("org_id"),
                                                skill_id=user_skill_data.get("skill_id"),
                                                endo=endo.get("endorsement"),
                                                description=endo.get("description"),
                                                proj_id=None,
                                                type=endo.get("type"))
                else:
                    db.create_skill_endorsement(endo_id=str(uuid4()),
                                                org_id=db.get_user(user_id).get("org_id"),
                                                skill_id=user_skill_data.get("skill_id"),
                                                endo=endo.get("endorsement"),
                                                description=endo.get("description"),
                                                proj_id=endo.get("proj_id"),
                                                type=endo.get("type"))
            returned_data = get_skills_by_users_id(user_id)
            return returned_data
        else:
            db.delete_user_endorsements(skill_id=skill_id, org_id=db.get_user(user_id).get("org_id"))
            returned_data = get_skills_by_users_id(user_id)
            return returned_data
    else:
        raise HTTPException(status_code=409, detail="Department not found for the user")


# SKILL_CATEGORIES

def get_skill_categories(user_id):
    user = db.get_user(user_id)
    org_id = user.get("org_id")
    org_skills = db.get_skills(org_id)
    skill_categories = db.get_skill_categories(org_id)

    for category in skill_categories:
        for key in org_skills:
            if org_skills[key].get("category_id") == category.get("value"):
                category["is_used"] = True
                break

    sorted_data = sorted(skill_categories, key=lambda x: x['label'])
    return sorted_data


def create_skill_category(data, user_id):
    skill_categories_data = data.model_dump()
    skill_category_id = str(uuid4())
    skill_categories_data["id"] = skill_category_id
    organization_id = db.get_user(user_id).get("org_id")
    db.create_skill_category(name=skill_categories_data.get("name"),
                             org_id=organization_id,
                             created_at=skill_categories_data.get("created_at"),
                             skill_category_id=skill_category_id)

    returned_data = get_skill_categories(user_id)

    return returned_data


def delete_skill_category(data, user_id):
    skill_categories_data = data.model_dump()
    skill_category_id = skill_categories_data.get("id")
    db.delete_skill_category(skill_category_id=skill_category_id)

    returned_data = get_skill_categories(user_id)

    return returned_data


def get_unused_skill_categories(user_id):
    returned_skill_categories = []
    already_used_skill_categories = []
    users = db.get_users()
    organization_id = users[user_id].get("org_id")

    org_skills = db.get_skills(organization_id)
    org_skill_categories = db.get_skill_categories(organization_id)

    for skill in org_skills:
        current_skill = org_skills[skill]
        already_used_skill_categories.append(current_skill.get("category_id"))

    for skill_category in org_skill_categories:
        if skill_category not in already_used_skill_categories:
            current_skill_category = org_skill_categories[skill_category]
            returned_custom_body = {
                "value": skill_category,
                "label": current_skill_category.get("name")
            }
            returned_skill_categories.append(returned_custom_body)
    return returned_skill_categories


def update_skill_category(data, user_id):
    user_skill_category_dict = data.model_dump()
    user_data = db.get_user(user_id)
    org_id = user_data.get("org_id")

    db.update_skill_category(id=user_skill_category_dict.get("id"),
                             org_id=org_id,
                             name=user_skill_category_dict.get("name"),
                             modified_at=user_skill_category_dict.get("modified_at"))

    returned_data = get_skill_categories(user_id)

    return returned_data


# DEPARTMENT_SKILLS
def get_department_skills():
    department_skills = db.get_department_skills()
    return department_skills


def create_department_skill(data, user_id):
    department_skills_data = data.model_dump()
    organization_id = db.get_user(user_id).get("org_id")
    departments = db.get_department(organization_id)
    department_skill_id = str(uuid4())
    for department in departments:
        current_department = departments[department]
        if str(current_department.get("manager_id")) == str(user_id):
            db.create_department_skill(dept_id=current_department.get("id"),
                                       skill_id=department_skills_data.get("skill_id"),
                                       id=department_skill_id)

            returned_data = get_organizations_skills(user_id)
            return returned_data


def delete_department_skill(data, user_id):
    removed_skill_id = data.model_dump().get("skill_id")
    department_skills = get_department_skills()
    for department in department_skills:
        current_department = department_skills[department]
        current_department_id = current_department.get("dept_id")
        current_department_skill_id = current_department.get("skill_id")
        if str(removed_skill_id) == current_department_skill_id:
            department_info = db.get_department_info(current_department_id)
            if str(department_info.get("manager_id")) == str(user_id):
                department_skill_ids = db.get_department_skill(removed_skill_id, current_department_id)

                for id in department_skill_ids:
                    db.delete_department_skill(id=id)

                returned_data = get_organizations_skills(user_id)
                return returned_data

# SKILLS PROPOSALS


def update_skill_proposal(data, user_id):
    update_data = data.model_dump()

    # Fetch organization and department id
    organization_id = db.get_user(user_id).get("org_id")
    departments = db.get_department(organization_id)

    # Find the department
    for dep in departments:
        current_department = departments[dep]
        if str(current_department.get("manager_id")) == user_id:
            department_id = dep

            # Fetch the skill proposals from his department
            proposed_skills = db.get_skill_proposals(department_id)
            for current_skill in proposed_skills:
                role_id = current_skill.get("role_id")
                skill_id = current_skill.get("skill_id")
                proposal = current_skill.get("proposal")
                # Check if the proposal is for project or for skill requests
                if skill_id and proposal:
                    if current_skill.get("user_id") == str(update_data.get("user_id")) and current_skill.get("skill_id") == str(update_data.get("skill_id")):
                        level = current_skill.get("level")
                        experience = current_skill.get("experience")
                        user_skill_exists = db.verify_user_skill(user_id=update_data.get("user_id"),
                                                                 skill_id=skill_id)
                        if user_skill_exists:
                            db.update_user_skill(user_id=update_data.get("user_id"),
                                                 skill_id=skill_id,
                                                 level=level,
                                                 experience=experience)
                        else:
                            db.create_user_skills(user_id=update_data.get("user_id"),
                                                  skill_id=skill_id,
                                                  level=level,
                                                  experience=experience,
                                                  created_at=datetime.now().isoformat())
                        db.delete_proposed_skill(user_id=update_data.get("user_id"), skill_id=skill_id)
                        return get_skill_proposals(user_id)
                elif role_id:
                    print("Entered Role")
                    if proposal:
                        # Make project assignment true
                        continue
                    else:
                        # Make project assignment false
                        continue
                else:
                    db.delete_proposed_skill(user_id=user_id, skill_id=skill_id)
                    return get_skill_proposals(user_id)


def get_skill_proposals(user_id):
    organization_id = db.get_user(user_id).get("org_id")
    # Find user department
    departments = db.get_department(organization_id)
    returned_skills = []
    # Check user department
    for dep in departments:
        department = departments[dep]
        if str(department.get("manager_id")) == user_id:
            skill_proposals = db.get_skill_proposals(dep)
            # Put the info in each proposal
            for skill_proposal in skill_proposals:
                # Check if it is skill proposal or project assignment
                role_ids = skill_proposal.get("role_ids")
                skill_id = skill_proposal.get("skill_id")
                if str(role_ids) == "None":
                    user_data = db.get_user(skill_proposal.get("user_id"))

                    # Put username in response
                    skill_proposal["user_name"] = user_data.get("name")
                    users_skills = get_skills_by_users_id(skill_proposal.get("user_id"))
                    if users_skills:
                        skill_proposal["type"] = "put"
                    else:
                        skill_proposal["type"] = "post"
                    skill_proposal["skill_name"] = db.get_skill_info(skill_id, organization_id).get("name")
                    returned_skills.append(skill_proposal)
                elif str(skill_id) == "None":
                    user_data = db.get_user(skill_proposal.get("user_id"))

                    # Put username in response
                    skill_proposal["user_name"] = user_data.get("name")

                    # Find the role and put it in response
                    team_roles = db.get_team_roles(organization_id)
                    for role in team_roles:
                        if str(role) in role_ids:
                            skill_proposal["role_name"] = team_roles[role].get("name")

                    # Find project details
                    assignment = db.get_assignment_info(skill_proposal.get("assignment_id"))
                    project = db.get_project_info(assignment.get("proj_id"))
                    skill_proposal["project_name"] = project.get("name")
                    skill_proposal["project_manager"] = db.get_user(project.get("manager_id")).get("name")
                    skill_proposal["work_hours"] = assignment.get("work_hours")
            return skill_proposals









