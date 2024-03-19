import re

from openai import OpenAI
from database.db import db
import os

openai_secretkey = os.environ["CHAT_SECRET_KEY"]
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", f"{openai_secretkey}"))
MODEL = "gpt-3.5-turbo"


def make_chat_gpt_request(data, user_id):
    # chat_data = data.model_dump()
    organization_id = db.get_user(user_id).get("org_id")
    #
    # additional_context = chat_data.get("context")
    # project_members = chat_data.get("project_members")
    # project = chat_data.get("project")
    #
    # all_details = db.get_all_details(org_id=organization_id, user_id=user_id)
    # projects = all_details.get("projects")
    # employee_assignments = all_details.get("employee_assignments")
    # team_roles = all_details.get("team_roles")
    #
    # system_message = (
    #     f"You are a team finder expert who needs to suggest the best team for a this project: {project}"
    #     "'tech_stack' contains the skills required for the project"
    #     "'team_roles' is very important, those are the roles that must be occupied by the team"
    #     "The 'count' for every role is the amount of employees needed with that role"
    #     "Everyone in the team must have at least one role, so there can't be more members than roles"
    #     "'available_roles' are the types of team_roles that are still available, this exists because there might already be members assigned to the project"
    #     "In the case that some roles are taken, you must recommend the best team with the reaming roles"
    #
    #     f"Here are all the members: {project_members}"
    #     "In the 'new' array you will find all the members that you can choose from"
    #     "'work_hours' are the amount of hours that the employee works daily"
    #     "0 work hours means fully available"
    #     "1-7 work hours mean partially available"
    #     "8 work hours means completely unavailable"
    #     "'deadline' represents the amount of weeks until an employees next deadline, meaning that they will be more available for a future project"
    #     "'dept_name' represents the department that the employee is in"
    #     "each user also has 'skills' with a level (1-5) and experience (1-6)"
    #
    #     "In the 'past' array you will find past members that have worked on the project, you can choose from these as well"
    #
    #     "In the 'proposed' array you will find employees that have already been proposed to work on the project"
    #     "You can use that information to make a better decision"
    #     "Also consider any team roles that have been proposed as team roles that are not available"
    #
    #     "In the 'active' array you will find employees that are already on the project"
    #     "The team_roles they occupy are not available"
    #     "Use this information to make a better decision"
    #
    #     "I'll give you some more information to help you make the best decision possible:"
    #
    #     f"Here are all the projects in the organization: {projects}"
    #     f"Here are all the employees assigned to projects: {employee_assignments}"
    #     f"Here are the organization team roles: {team_roles} "
    #
    #     f"The response should be your best recommendation of team for this project sent as a list of employees UUID's"
    #
    #     "If you can't determine a full team to fill the remaining positions you should return an empty JSON list"
    #     "I must mention that this is a worst-case scenario. I prefer a weak team over no team. So try your best to come up with something"
    #     "But if you can't come up with a team that satisfies the manager's condition, return an empty list"
    # )
    #
    # user_message = (f"The manager of the project himself has also sent a comment: '{additional_context}'."
    #                 "Do your best to satisfy his preferences when assembling your team"
    #                 "Make sure not to return more users than required roles")
    #
    # response = client.chat.completions.create(
    #     model=MODEL,
    #     messages=[
    #         {"role": "system", "content": system_message},
    #         {"role": "user", "content": user_message},
    #     ],
    #     temperature=0,
    # )
    # uuids = re.findall(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', response.choices[0].message.content)
    uuids = ["525fcb70-f82d-4f4c-9082-b4c8757ee585", "e0d59842-82c2-417c-8374-e2e64e02ad63", "5f67126a-247b-4b5f-aec6-f5746b04a96d", "b3048d33-a96a-4c2b-825d-c34388a091a1",
             "dc98d424-ddea-4949-9ac4-190233d00b82","44d1f602-97b4-4bbb-8db8-9602de38fa02"]
    # Fetch user details
    project_assignments = db.get_project_assignments(organization_id)
    returned_employees = []
    for user in uuids:
        employee = {
            "user_id": user,
            "name": db.get_user(user).get("name")
        }
        if project_assignments:
            for assignment in project_assignments:
                if str(assignment.get("user_id")) == str(user):
                    employee["deadline_date"] = assignment.get("deadline_date")
                    employee["work_hours"] = assignment.get("work_hours")
                else:
                    employee["deadline_date"] = None
                    employee["work_hours"] = 0
                employee["name"] = db.get_user(user).get("name")

                # Get user skills
                users_skills = db.get_user_skills(user)
                for skill in users_skills:
                    skill_info = db.get_skill(skill.get("skill_id"))
                    skill['name'] = skill_info.get("name")
                    del skill['created_at'], skill['skill_id'], skill['user_id']
                employee["skills"] = users_skills
            returned_employees.append(employee)
        else:
            employee["deadline_date"] = None
            employee["work_hours"] = 0
            users_skills = db.get_user_skills(user)
            for skill in users_skills:
                skill_info = db.get_skill(skill.get("skill_id"))
                skill['name'] = skill_info.get("name")
                del skill['created_at'], skill['skill_id'], skill['user_id']
            employee["skills"] = users_skills
            returned_employees.append(employee)
    return returned_employees




