import json

from openai import OpenAI
from database.db import db
import os
from typing import Dict
from openai_feature.models import UserResponse

response_model ={ "user_id": "abc51a44-cd8b-4835-afad-2a3af477efbd",
            "name": "Emily Brown",
            "roles": [
                {
                    "id": "af617841-728c-4eb6-8af5-3162d0dc91db",
                    "name": "Programmer"
                }
            ],
            "skills": [
                {
                    "name": "C++",
                    "experience": 3,
                    "level": 3
                },
                {
                    "name": "Swift",
                    "experience": 6,
                    "level": 3
                }
            ],
            "dept_name": "Frontend",
            "current_work_hours": 1,
            "work_hours": 1}

openai_secretkey = os.environ["CHAT_SECRET_KEY"]
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", f"{openai_secretkey}"))
MODEL = "gpt-3.5-turbo"


def make_chat_gpt_request(data, user_id):
    chat_data = data.model_dump()
    organization_id = db.get_user(user_id).get("org_id")

    additional_context = chat_data.get("context")
    project_members = chat_data.get("project_members")
    project = chat_data.get("project")

    all_details = db.get_all_details(org_id=organization_id)
    system_message = (
        f"You are a team finder expert who suggests the best team for this project: {project}"
        "All the current team members are in an array called 'new'"
        "All the past team members are in an array called 'past'"
        "All the new team members that have already been proposed are in an array called 'proposed'"
        "All the new team members that you can choose from are in an array called 'new'"
        f"Here are all the members: {project_members} "
        f"For additional context, this is the whole database: {all_details}."
        f"The response should be structured in this format {response_model}, "
        "The response should be ONLY a json list of employees from 'new' members in that format"
        "The response should not contain unnecessary spaces or end lines, so that it can be easily mapped to a list of employees (the team)."
        "You should look at the team_roles required for the project and return a team that fills all the roles that haven't already been taken"
        "If you can't determine a full remaining team you should return an empty"
        "If you can't determine a full remaining team you should return an empty list in JSON, but this is a worst-case scenario. I prefer a weak team over no team"
    )

    user_message = (f"The project manager also sent his comment: {additional_context}."
                    "You should take his comment into consideration when deciding the team")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)




