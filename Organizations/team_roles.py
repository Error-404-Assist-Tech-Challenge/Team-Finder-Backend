from fastapi import APIRouter, Depends, HTTPException
from typing import List
from auth import AuthHandler
from Organizations.models import TeamRole, TeamRoleCreate, TeamRoleUpdate, TeamRoleDelete, TeamRoleAll
from Organizations.utils import *

auth_handler = AuthHandler()
team_roles_router = APIRouter()


@team_roles_router.post("/api/organizations/team_roles", response_model=List[TeamRole])
def create_team_role_route(team_role_data: TeamRoleCreate, admin_id: str = Depends(auth_handler.auth_wrapper)):
    return create_team_role(team_role_data, admin_id)


@team_roles_router.put("/api/organizations/team_roles", response_model=List[TeamRole])
def update_team_role_route(team_role_data: TeamRoleUpdate, admin_id: str = Depends(auth_handler.auth_wrapper)):
    return update_team_role(team_role_data, admin_id)


@team_roles_router.delete("/api/organizations/team_roles", response_model=List[TeamRole])
def delete_team_role_route(team_role_data: TeamRoleDelete, admin_id: str = Depends(auth_handler.auth_wrapper)):
    response, error = delete_team_role(team_role_data, admin_id)
    if error:
        raise HTTPException(status_code=500, detail=error)
    return response


@team_roles_router.get("/api/organizations/team_roles", response_model=List[TeamRole])
def team_roles_get(admin_id: str = Depends(auth_handler.auth_wrapper)):
    return get_team_roles(admin_id)


@team_roles_router.get("/api/organizations/team_roles/all", response_model=List[TeamRoleAll])
def team_roles_get(admin_id: str = Depends(auth_handler.auth_wrapper)):
    return get_all_team_roles(admin_id)
