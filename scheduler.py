from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dateutil.relativedelta import relativedelta
from database.db import db
import uuid

from Skills.utils import get_employee_skill_proposals


def delete_expired_signup_tokens():
    signup_tokens = db.get_signup_tokens()
    format = "%Y-%m-%d %H:%M:%S"
    current_time = datetime.utcnow()

    for token in signup_tokens:
        if datetime.strptime(token.get("expires_at"), format) < current_time:
            db.delete_signup_token(token.get("id"))


def delete_expired_password_reset_tokens():
    password_reset_tokens = db.get_password_reset_tokens()
    format = "%Y-%m-%d %H:%M:%S"
    current_time = datetime.utcnow()

    for token in password_reset_tokens:

        if datetime.strptime(token.get("expires_at"), format) < current_time:
            db.delete_password_reset_token(token.get("id"))


def propose_user_skill_update():
    organizations = db.get_organizations()
    for org_id in organizations:
        projects = db.get_org_projects(org_id)
        departments = db.get_department(org_id)

        for proj_id in projects:
            project = projects[proj_id]
            required_skills = db.get_project_tech_stack_skills(proj_id, org_id)
            project_members = db.get_project_approved_members(proj_id)

            for member in project_members:
                user_id = member.get("user_id")
                member_skills = db.get_user_skills(user_id)
                department = db.get_department_user(user_id)
                department_info = db.get_department_info(department)

                if department_info is None:
                    # If employee isn't found as a department member check if he manages one
                    for key in departments:
                        if str(departments[key].get("manager_id")) == str(user_id):
                            department_info = departments[key]

                if department_info:
                    department_skills = db.get_department_skills(department_info.get("id"))
                    eligible_skills = []
                    eligible_user_skills = []

                    # Check for skills required by the project that are also in the department skills
                    for skill in required_skills:
                        if str(skill.get("skill_id")) in department_skills:
                            eligible_skills.append(skill.get("skill_id"))

                    # Check for user skills that match the eligible skills
                    for skill in member_skills:
                        if str(skill.get("skill_id")) in eligible_skills:
                            eligible_user_skills.append(skill)
                            eligible_skills.remove(skill.get("skill_id"))

                    user_proposed_skills = get_employee_skill_proposals(user_id)

                    user_proposed_skills_ids = []
                    for proposed_skill in user_proposed_skills:
                        user_proposed_skills_ids.append(proposed_skill.get("skill_id"))

                    # Propose new skills that are in the project skill
                    # requirements and in the department, but not assigned to user
                    for skill_id in eligible_skills:
                        if skill_id not in user_proposed_skills_ids:
                            id = uuid.uuid4()
                            db.propose_skill(id=id,
                                             proposal=False,
                                             skill_id=skill_id,
                                             user_id=user_id,
                                             dept_id=department_info.get("id"),
                                             level=1,
                                             experience=1,
                                             for_employee=True,
                                             read=False)

                    # Propose skill updates for the user based on their existing skills
                    for skill in eligible_user_skills:
                        # Check if the skill has already been proposed for the user
                        proposed_skill = False
                        for proposal in user_proposed_skills:
                            if str(proposal.get("skill_id")) == str(skill.get("skill_id")):
                                proposed_skill = True
                                break

                        if proposed_skill:
                            continue

                        skill_level = int(skill.get("level"))
                        skill_experience = int(skill.get("experience"))

                        # Determine the proposed level of the skill
                        if skill_level < 5:
                            proposed_level = skill_level + 1
                        else:
                            proposed_level = skill_level

                        # Determine the proposed experience of the skill
                        if skill_experience < 6:
                            skill_created_at = skill.get("created_at")
                            if '.' not in skill_created_at:
                                skill_created_at += '.00'
                            created_at_date = datetime.strptime(skill_created_at, '%Y-%m-%d %H:%M:%S.%f')
                            current_date = datetime.utcnow()
                            experience_duration = current_date - created_at_date
                            experience_months = experience_duration.days / 30

                            if experience_months > 6:
                                proposed_experience = skill_experience + 1
                            else:
                                proposed_experience = skill_experience
                        else:
                            proposed_experience = skill_experience

                        if proposed_skill is not None and proposed_experience is not None:
                            id = uuid.uuid4()
                            db.propose_skill(id=id,
                                             proposal=False,
                                             skill_id=skill.get("skill_id"),
                                             user_id=user_id,
                                             dept_id=department_info.get("id"),
                                             level=proposed_level,
                                             experience=proposed_experience,
                                             for_employee=True,
                                             read=False)


def deactivate_demo_accounts():
    organizations = db.get_organizations_demo()

    format = '%Y-%m-%d %H:%M:%S.%f'
    current_time = datetime.utcnow()
    for organization in organizations:
        current_organization = organizations[organization]
        if current_organization.get("demo") == "True" or current_organization.get("demo") == "unpaid":
            created_at = datetime.strptime(current_organization.get("created_at"), format)
            org_created_at = created_at + relativedelta(months=3)
            if org_created_at > current_time:
                db.deactivate_account(current_organization.get("id"))


scheduler = BackgroundScheduler()

scheduler.add_job(deactivate_demo_accounts, "interval", seconds=4)
scheduler.add_job(delete_expired_signup_tokens, "interval", hours=12)
scheduler.add_job(delete_expired_password_reset_tokens, "interval", hours=12)
scheduler.add_job(propose_user_skill_update, "interval", hours=1)
