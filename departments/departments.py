from fastapi import APIRouter
from departments.models import Departament
from departments.utils import *

departments_router = APIRouter()


@departments_router.post("/api/departments", response_model=Departament)
def create_departament(departament_data: Departament):
    return departament_data


@departments_router.get("/api/departments")
def departments_get():
    return get_departments()
