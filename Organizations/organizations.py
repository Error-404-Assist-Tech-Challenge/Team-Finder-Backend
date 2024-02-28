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
def organization_get_skills(user_id):
    return get_organizations_skills(user_id)


@organization_router.post("/api/organizations/signup_token")
def signup_token_create(org_id: UUID):
    return create_signup_token(org_id)


@organization_router.get("/api/organizations/signup_tokens")
def signup_tokens_get(org_id: UUID):
    return get_organization_signup_tokens(org_id)

