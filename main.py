from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

from websocket.manager import ConnectionManager

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

from scheduler import scheduler


app = FastAPI()
manager = ConnectionManager()

origins = ["http://localhost:5173", "https://localhost:5174", "https://team-finder-404.web.app"]

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


@app.websocket("/ws/{access_token}")
async def websocket_endpoint(websocket: WebSocket, access_token: str):
    await manager.connect(websocket, access_token=access_token)

    try:
        while True:
            message = await websocket.receive_text()
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn

    scheduler.start()

    uvicorn.run(app, host="0.0.0.0", port=8000)
