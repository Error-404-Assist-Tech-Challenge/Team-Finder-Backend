from fastapi import APIRouter
from user.models import UserCreate
from user.utils import get_users
user_router = APIRouter()


@user_router.post("/api/authenticate", response_model=UserCreate)
def authenticate_user(user_data: UserCreate):
    return user_data

@user_router.get("/api/users/get")
def users_get():
    return get_users()