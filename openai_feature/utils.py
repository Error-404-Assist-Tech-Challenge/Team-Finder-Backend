from openai import OpenAI
from database.db import db
import os
from typing import Dict

openai_secretkey = os.environ["CHAT_SECRET_KEY"]
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", f"{openai_secretkey}"))
MODEL = "gpt-3.5-turbo"
def make_chat_gpt_request(data) -> Dict[str, str]:
    all_details = db.get_all_details()

    system_message = f"You are a team finder expert who suggests the best team made out of 5 persons. This is all the database {all_details}."
    user_message = ("Can you make the best team made out of 5 developers from the database."
                    f" If you don't find them, tell us that we lack developers. Details of the user{data.details} and the skills needed: {data.skills}"
                    "The message should be a dictionary")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    return {
        "system_message": system_message,
        "user_message": user_message,
        "chat_response": response.choices[0].message.content,
        "details": data.details,
        "skills": data.skills
    }




