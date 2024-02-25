from fastapi import APIRouter
from users.models import UserCreate
from users.utils import create_user, get_users

user_router = APIRouter()


@user_router.post("/api/user", response_model=UserCreate)
def create_user_route(user_data: UserCreate):
    return create_user(user_data)


@user_router.get("/api/users")
def users_get():
    return get_users()
