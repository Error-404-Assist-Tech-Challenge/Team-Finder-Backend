from fastapi import APIRouter
from Projects.models import Project_tech_stack_skills
from Projects.utils import create_project_tech_stack_skill, get_project_tech_stack_skills

project_tech_stack_skills_router = APIRouter()


@project_tech_stack_skills_router.post("/api/project_tech_stack_skills", response_model=Project_tech_stack_skills)
def create_project_tech_stack_skills_route(project_tech_stack_skills_data: Project_tech_stack_skills):
    return create_project_tech_stack_skill(project_tech_stack_skills_data)


@project_tech_stack_skills_router.get("/api/project_tech_stack_skills")
def project_tech_stack_skills_get():
    return get_project_tech_stack_skills()
