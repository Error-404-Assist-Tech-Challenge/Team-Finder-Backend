from fastapi import APIRouter
from roles.models import Roles
from roles.utils import *

roles_router = APIRouter()


@roles_router.post("/api/roles", response_model=Roles)
def create_role_route(user_role_data: Roles):
    return create_role(user_role_data)


@roles_router.get("/api/roles")
def roles_get():
    return get_roles()
