from openai import OpenAI
from database.db import db
import os
from typing import Dict

openai_secretkey = os.environ["CHAT_SECRET_KEY"]
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", f"{openai_secretkey}"))
MODEL = "gpt-3.5-turbo"


#     active: Optional[List[str]]
#     new: Optional[List[str]]
#     past: Optional[List[str]]
#     proposed: Optional[List[str]]
#
#
# class Chat_basemodel(BaseModel):
#     context: str
#     project_members: Project_Members
#     project: str


def make_chat_gpt_request(data, user_id):
    chat_data = data.model_dump()
    organization_id = db.get_user(user_id).get("org_id")

    additional_context = chat_data.get("context")
    project_members = chat_data.get("project_members")
    project = chat_data.get("project")

    print(additional_context)
    print(project_members)
    print(project)


    # all_details = db.get_all_details(user_id=user_id,org_id=organization_id)
    # system_message = (f"You are a team finder expert who suggests the best team made out of 5 persons."
    #                   f" This is all the database: {all_details}"
    #                   f"The response should be structured as JSON, "
    #                   f"so that it can be easily mapped to a list of employees (the team)."
    #                   f"If you don't find them, return an empty JSON list."
    #                   f"")
    # user_message = (f"{additional_context}"
    #                 f"  Details of the user{data.details} and the skills needed: {data.skills}")
    #
    # response = client.chat.completions.create(
    #     model=MODEL,
    #     messages=[
    #         {"role": "system", "content": system_message},
    #         {"role": "user", "content": user_message},
    #     ],
    #     temperature=0,
    # )
    # return {
    #     "system_message": system_message,
    #     "user_message": user_message,
    #     "chat_response": response.choices[0].message.content,
    #     "details": data.details,
    #     "skills": data.skills
    # }




