from fastapi import APIRouter, Depends, HTTPException
from auth import AuthHandler
from Users.models import AdminCreate, AuthResponse, EmployeeCreate, UserLogin, TokenResponse
from Users.utils import create_admin, create_employee, get_users, login_user, account_exists

auth_handler = AuthHandler()
user_router = APIRouter()


@user_router.post("/api/users/admin", response_model=AuthResponse)
def admin_create(user_data: AdminCreate):
    if not account_exists(user_data):
        admin_obj, error = create_admin(user_data)
        if error:
            raise HTTPException(status_code=500, detail="Failed to create user: " + error)
        access_token, refresh_token = auth_handler.generate_tokens(admin_obj.get("id"))
        admin_obj["access_token"] = access_token
        admin_obj["refresh_token"] = refresh_token
        return admin_obj
    else:
        raise HTTPException(status_code=409, detail="User with this email already exists")


@user_router.get("/api/users/refresh_token", response_model=TokenResponse)
def refresh_token(token: str = Depends(auth_handler.refresh_auth_wrapper)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing refresh token")
    return {"access_token": token}


@user_router.get("/api/users/protected")
def protected(user_id: str = Depends(auth_handler.auth_wrapper)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"user_id": user_id}


@user_router.post("/api/users/employee", response_model=AuthResponse)
def employee_create(user_data: EmployeeCreate):
    if not account_exists(user_data):
        employee_obj, error = create_employee(user_data)
        if error:
            raise HTTPException(status_code=409, detail=error)
        access_token, refresh_token = auth_handler.generate_tokens(employee_obj.get("id"))
        employee_obj["access_token"] = access_token
        employee_obj["refresh_token"] = refresh_token
        return employee_obj
    else:
        raise HTTPException(status_code=409, detail="User with this email already exists")


@user_router.post("/api/users/login", response_model=AuthResponse)
def user_login(user_data: UserLogin):
    login_obj, error = login_user(user_data)
    if error:
        raise HTTPException(status_code=409, detail=error)
    else:
        access_token, refresh_token = auth_handler.generate_tokens(login_obj.get("id"))
        login_obj["access_token"] = access_token
        login_obj["refresh_token"] = refresh_token
    return login_obj


@user_router.get("/api/users")
def users_get(user_id: str):
    return get_users(user_id)
