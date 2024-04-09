from fastapi import APIRouter, Depends
from Organizations.models import UserRole
from Organizations.utils import *
from auth import AuthHandler

user_roles_router = APIRouter(tags=["Organizations"])
auth_handler = AuthHandler()


@user_roles_router.post("/api/organizations/user_roles", response_model=UserRole)
def create_user_role_route(user_role_data: UserRole):
    return create_user_role(user_role_data)


@user_roles_router.get("/api/organizations/user_roles")
def user_roles_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_user_roles(user_id)
