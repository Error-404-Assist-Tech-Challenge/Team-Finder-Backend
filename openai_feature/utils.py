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

    all_details = db.get_all_details(user_id=user_id,org_id=organization_id)
    system_message = (
        "You are a team finder expert who suggests the best team made out of 5 persons. "
        f"This is all the database: {all_details}. "
        f"The response should be structured as this Response Model {response_model}, "
        "the response should be returned like this and remove any other information except the JSON containing all the employees. "
        "The response should not contain unnecessary spaces or end lines, so that it can be easily mapped to a list of employees (the team). "
        "If you don't find them, return an empty JSON list."
    )

    user_message = (f"This is the context provided by the project manager: {additional_context}."
                    f"This is the project that he created: {project}"
                    f"And these are the project members: {project_members}")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)




