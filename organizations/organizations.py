from fastapi import APIRouter
from organizations.models import Organization
from organizations.utils import *

organization_router = APIRouter()


@organization_router.post("/api/organizations", response_model=Organization)
def create_organization(organization_data: Organization):
    return organization_data


@organization_router.get("/api/organizations")
def organization_get():
    return get_organizations()
