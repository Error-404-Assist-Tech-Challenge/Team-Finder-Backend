from fastapi import APIRouter, Depends
from Skills.models import Department_skills, Remove_department_skill
from Skills.utils import create_department_skill, get_department_skills, delete_department_skill
from auth import AuthHandler

auth_handler = AuthHandler()
department_skills_router = APIRouter()


@department_skills_router.post("/api/skills/department")
def department_skill_create(department_skills_data: Department_skills, user_id: str = Depends(auth_handler.auth_wrapper)):
    return create_department_skill(department_skills_data, user_id)


@department_skills_router.get("/api/skills/department")
def department_skills_get():
    return get_department_skills()


@department_skills_router.delete("/api/skills/department")
def department_skill_delete(removed_data: Remove_department_skill, user_id: str = Depends(auth_handler.auth_wrapper)):
    return delete_department_skill(removed_data, user_id)


