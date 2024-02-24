from fastapi import APIRouter
from organization.models import Organization
#from organization.utils import get_users

organization_router = APIRouter()


@organization_router.post("/api/authenticate", response_model=Organization)
def create_organization(organization_data: Organization):
    return organization_data

@organization_router.get("/api/organization/get")
def organization_get():
    return organization_get()