from fastapi import APIRouter, Depends, HTTPException

from auth import AuthHandler
from Organizations.models import RoleCreate, RoleData
from Organizations.utils import *

auth_handler = AuthHandler()
organization_roles_router = APIRouter()


@organization_roles_router.post("/api/organizations/roles", response_model=RoleCreate)
def organization_user_role_create(data: RoleCreate, admin_id: str = Depends(auth_handler.auth_wrapper)):
    data, error = create_organization_user_role(data, admin_id)
    if error:
        raise HTTPException(status_code=409, detail=error)
    return data


@organization_roles_router.get("/api/organizations/roles")
def organization_roles_get():
    return get_organization_roles()
