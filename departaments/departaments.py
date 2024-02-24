from fastapi import APIRouter
from departaments.models import Departament

departaments_router = APIRouter()


@departaments_router.post("/api/authenticate", response_model=Departament)
def create_departament(departament_data: Departament):
    return departament_data

@departaments_router.get("/api/departament/get")
def departaments_get():
    return departaments_get()
