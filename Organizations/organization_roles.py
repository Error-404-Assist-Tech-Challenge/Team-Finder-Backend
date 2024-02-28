from fastapi import APIRouter
from Organizations.models import Organization_roles
from Organizations.utils import *

organization_roles_router = APIRouter()


@organization_roles_router.post("/api/organizations/roles", response_model=Organization_roles)
def create_organization_role_route(organization_data: Organization_roles):
    return create_organization_role(organization_data)


@organization_roles_router.get("/api/organizations/roles")
def organization_roles_get():
    return get_organization_roles()
