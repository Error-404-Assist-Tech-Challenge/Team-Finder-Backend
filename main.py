from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from openai_feature.chat_gpt_feature import chat_gpt_router
from Skills.skill_categories import skill_categories_router
from Skills.skills import skills_router
from Skills.user_skills import user_skills_router
from users.users import user_router
from user_roles.user_roles import user_roles_router
from departments.departments import departments_router
from department_members.department_members import department_members_router
from organizations.organizations import organization_router
from organization_members.organization_members import organization_members_router
from roles.roles import roles_router
from Skills.department_skills import department_skills_router

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
app.include_router(organization_members_router)
app.include_router(departments_router)
app.include_router(department_members_router)
app.include_router(chat_gpt_router)
app.include_router(user_skills_router)
app.include_router(skills_router)
app.include_router(skill_categories_router)
app.include_router(roles_router)
app.include_router(department_skills_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
