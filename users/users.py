from fastapi import APIRouter
from users.models import UserCreate
from users.utils import *

user_router = APIRouter()


@user_router.post("/api/users", response_model=UserCreate)
def create_user(user_data: UserCreate):
    return create_user(user_data)


@user_router.get("/api/users")
def users_get():
    return get_users()
