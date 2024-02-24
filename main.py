from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from departaments.departaments import departaments_router
from organization.organization import organization_router
from user.user import user_router

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
app.include_router(organization_router)
app.include_router(departaments_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
