from fastapi import APIRouter
from Skills.models import Department_skills
from Skills.utils import create_department_skill, get_department_skills

department_skills_router = APIRouter()


@department_skills_router.post("/api/department_skills", response_model=Department_skills)
def create_department_skill_route(department_skills_data: Department_skills):
    return create_department_skill(department_skills_data)


@department_skills_router.get("/api/department_skills")
def department_skills_get():
    return get_department_skills()
