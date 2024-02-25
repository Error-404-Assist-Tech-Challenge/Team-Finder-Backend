from fastapi import APIRouter
from user_roles.models import UserRole
from user_roles.utils import *

user_roles_router = APIRouter()


@user_roles_router.post("/api/user_roles", response_model=UserRole)
def create_user_role_route(user_role_data: UserRole):
    return create_user_role(user_role_data)


@user_roles_router.get("/api/user_roles")
def user_roles_get():
    return get_user_roles()
