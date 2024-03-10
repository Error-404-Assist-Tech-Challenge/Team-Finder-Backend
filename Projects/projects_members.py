from fastapi import APIRouter, Depends
from typing import List
from auth import AuthHandler
from Projects.models import Project_members, Search, SearchResponse
from Projects.utils import create_project_member, get_project_members, search_employees

auth_handler = AuthHandler()
project_members_router = APIRouter()


@project_members_router.post("/api/projects/project_members", response_model=Project_members)
def create_project_members_route(project_members_data: Project_members):
    return create_project_member(project_members_data)


@project_members_router.get("/api/projects/project_members")
def project_members_get():
    return get_project_members()


@project_members_router.get("/api/projects/search_employees", response_model=List[SearchResponse])
def employees_search_get(search_data: Search, user_id: str = Depends(auth_handler.auth_wrapper)):
    return search_employees(search_data, user_id)
