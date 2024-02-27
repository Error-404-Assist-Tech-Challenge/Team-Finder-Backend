from fastapi import APIRouter
from Organizations.models import Team_roles
from Organizations.utils import *

team_roles_router = APIRouter()


@team_roles_router.post("/api/team_roles", response_model=Team_roles)
def create_team_role_route(team_role_data: Team_roles):
    return create_team_role(team_role_data)


@team_roles_router.get("/api/team_roles")
def team_roles_get():
    return get_team_roles()
