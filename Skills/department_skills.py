from fastapi import APIRouter, Depends
from Skills.models import Department_skills
from Skills.utils import create_department_skill, get_department_skills, update_department_skills
from auth import AuthHandler

auth_handler = AuthHandler()
department_skills_router = APIRouter()


@department_skills_router.post("/api/skills/department", response_model=Department_skills)
def department_skill_create(department_skills_data: Department_skills):
    return create_department_skill(department_skills_data)


@department_skills_router.get("/api/skills/department")
def department_skills_get():
    return get_department_skills()


@department_skills_router.put("/api/skills/department")
def department_skills_update(department_skill_data: Department_skills):
    return update_department_skills(department_skill_data)
