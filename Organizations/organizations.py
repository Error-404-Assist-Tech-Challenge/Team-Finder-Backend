from fastapi import APIRouter, Depends, HTTPException
from typing import List

from auth import AuthHandler
from Organizations.models import Organization, OrganizationMember, ModifiedSkill
from Organizations.utils import *

auth_handler = AuthHandler()
organization_router = APIRouter()


@organization_router.post("/api/organizations", response_model=Organization)
def create_organization_route(organization_data: Organization):
    return create_organization(organization_data)


@organization_router.get("/api/organizations")
def organization_get():
    return get_organizations()


#ORGANIZATION SKILL ENDPOINTS
@organization_router.get("/api/organizations/skills")
def organization_get_skills(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_organizations_skills(user_id)


@organization_router.get("/api/organizations/skills/unused")
def organization_get_skills(user_id: str = Depends(auth_handler.auth_wrapper)):
    return get_unused_organization_skills(user_id)

@organization_router.put("/api/organizations/skills")
def organization_get_skills(modified_skill_data: ModifiedSkill, user_id: str = Depends(auth_handler.auth_wrapper)):
    return update_organization_skill(modified_skill_data, user_id)


#ORGANIZATION USERS


@organization_router.get("/api/organization/users", response_model=List[OrganizationMember])
def organization_get_skills(admin_id: str = Depends(auth_handler.auth_wrapper)):
    return get_org_users(admin_id)


@organization_router.post("/api/organizations/signup_token")
def signup_token_create(user_id: str = Depends(auth_handler.auth_wrapper)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication failed")
    token, error = create_signup_token(user_id)

    if error:
        raise HTTPException(status_code=500, detail=error)
    return token


@organization_router.get("/api/organizations/signup_tokens")
def signup_tokens_get(user_id: str = Depends(auth_handler.auth_wrapper)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication failed")

    return get_organization_signup_tokens(user_id)


@organization_router.get("/api/organizations/verify_signup_token")
def signup_token_verify(id: str):
    response, error = verify_signup_token(id)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return response
