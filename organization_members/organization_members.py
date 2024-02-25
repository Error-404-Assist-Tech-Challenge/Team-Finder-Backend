from fastapi import APIRouter
from organization_members.models import Organization_member
from organization_members.utils import create_organization_member, get_organization_members

organization_members_router = APIRouter()

@organization_members_router.post("/api/organization_members", response_model=Organization_member)
def create_organization_member_route(organization_member_data: Organization_member):
    return create_organization_member(organization_member_data)

@organization_members_router.get("/api/organization_members")
def organization_members_get():
    return get_organization_members()
