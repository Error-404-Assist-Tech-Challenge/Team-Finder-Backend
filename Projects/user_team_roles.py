from fastapi import APIRouter
from Projects.models import User_team_roles
from Projects.utils import create_user_team_role, get_user_team_roles

user_team_roles_router = APIRouter(tags=["Projects"])


@user_team_roles_router.post("/api/projects/user_team_roles", response_model=User_team_roles)
def create_user_team_roles_route(user_team_roles_data: User_team_roles):
    return create_user_team_role(user_team_roles_data)


@user_team_roles_router.get("/api/projects/user_team_roles")
def user_team_roles_get():
    return get_user_team_roles()
