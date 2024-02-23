from fastapi import APIRouter
from user.models import UserCreate

user_router = APIRouter()


@user_router.post("/api/authenticate", response_model=UserCreate)
def authenticate_user(user_data: UserCreate):
    return user_data
