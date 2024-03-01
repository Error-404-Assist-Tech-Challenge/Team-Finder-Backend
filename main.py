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

from Projects.projects import projects_router
from Projects.projects_assignments import project_assignments_router
from Projects.projects_members import project_members_router
from Projects.project_needed_roles import project_needed_roles_router
from Projects.user_team_roles import user_team_roles_router
from Projects.project_tech_stack_skills import project_tech_stack_skills_router

app = FastAPI()

origins = ["http://localhost:5173", "https://jubilant-waffle-j9rp64qr47hp49r-5173.app.github.dev"]

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
app.include_router(projects_router)
app.include_router(project_assignments_router)
app.include_router(project_members_router)
app.include_router(project_needed_roles_router)
app.include_router(user_team_roles_router)
app.include_router(project_tech_stack_skills_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
