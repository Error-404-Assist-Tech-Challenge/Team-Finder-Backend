from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Users.users import user_router

from openai_feature.chat_gpt_feature import chat_gpt_router

from Skills.skill_categories import skill_categories_router
from Skills.skills import skills_router
from Skills.user_skills import user_skills_router
from Skills.department_skills import department_skills_router

from Organizations.user_roles import user_roles_router
from Organizations.organizations import organization_router
from Organizations.organization_roles import organization_roles_router
from Organizations.team_roles import team_roles_router

from Departments.departments import departments_router
from Departments.department_members import department_members_router


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(user_roles_router)
app.include_router(organization_router)
app.include_router(departments_router)
app.include_router(department_members_router)
app.include_router(chat_gpt_router)
app.include_router(user_skills_router)
app.include_router(skills_router)
app.include_router(skill_categories_router)
app.include_router(department_skills_router)
app.include_router(organization_roles_router)
app.include_router(team_roles_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
