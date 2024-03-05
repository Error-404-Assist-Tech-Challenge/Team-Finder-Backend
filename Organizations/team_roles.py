from fastapi import APIRouter, Depends, HTTPException

from auth import AuthHandler
from Organizations.models import TeamRole, TeamRoleUpdate, TeamRoleDelete
from Organizations.utils import *

auth_handler = AuthHandler()
team_roles_router = APIRouter()


@team_roles_router.post("/api/organizations/team_roles", response_model=TeamRole)
def create_team_role_route(team_role_data: TeamRole, admin_id: str = Depends(auth_handler.auth_wrapper)):
    return create_team_role(team_role_data, admin_id)


@team_roles_router.put("/api/organizations/team_roles")
def update_team_role_route(team_role_data: TeamRoleUpdate, admin_id: str = Depends(auth_handler.auth_wrapper)):
    return update_team_role(team_role_data)


@team_roles_router.delete("/api/organizations/team_roles")
def delete_team_role_route(team_role_data: TeamRoleDelete, admin_id: str = Depends(auth_handler.auth_wrapper)):
    response, error = delete_team_role(team_role_data)
    if error:
        raise HTTPException(status_code=500, detail=error)
    return response


@team_roles_router.get("/api/organizations/team_roles")
def team_roles_get(admin_id: str = Depends(auth_handler.auth_wrapper)):
    return get_team_roles(admin_id)
