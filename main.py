from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users.users import user_router
from user_roles.user_roles import user_roles_router
from departments.departments import departments_router
from organizations.organizations import organization_router

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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
