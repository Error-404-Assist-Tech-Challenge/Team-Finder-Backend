from uuid import UUID

from fastapi import APIRouter
from Organizations.models import Organization
from Organizations.utils import *

organization_router = APIRouter()


@organization_router.post("/api/organizations", response_model=Organization)
def create_organization_route(organization_data: Organization):
    return create_organization(organization_data)


@organization_router.get("/api/organizations")
def organization_get():
    return get_organizations()

@organization_router.get("/api/organizations/skills")
def organization_get_skills(organization_id: str):
    return get_organizations_skills(organization_id)

