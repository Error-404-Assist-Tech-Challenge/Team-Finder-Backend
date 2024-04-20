from fastapi import APIRouter, Response, Depends, Cookie, HTTPException
from functools import partial

from auth import AuthHandler
from websocket.manager import ConnectionManager
from Users.models import AdminCreate, AuthResponse, EmployeeCreate, UserLogin, PasswordReset
from Users.utils import create_admin, create_employee, get_user, login_user, account_exists, create_password_reset_token, reset_password

auth_handler = AuthHandler()
connection_manager = ConnectionManager()
user_router = APIRouter(tags=["Users"])

# Create a partial function with disconnect_websocket set to True
auth_wrapper_with_params = partial(auth_handler.auth_wrapper, disconnect_websocket=True)


@user_router.post("/api/users/admin", response_model=AuthResponse)
def admin_create(user_data: AdminCreate, response: Response):
    if not account_exists(user_data):
        admin_obj, error = create_admin(user_data)
        if error:
            raise HTTPException(status_code=500, detail="Failed to create user: " + error)
        access_token, refresh_token = auth_handler.generate_tokens(admin_obj.get("id"))
        del admin_obj["id"]
        admin_obj["access_token"] = access_token
        response.set_cookie(key="refresh_token", value=refresh_token, secure=True, httponly=True, domain=".koyeb.app", path="/api", samesite="none")

        return admin_obj
    else:
        raise HTTPException(status_code=409, detail="User with this email already exists")


@user_router.get("/api/users/refresh_token", response_model=AuthResponse)
def refresh_token(refresh_token: str | None = Cookie(None)):
    token, user_id = auth_handler.refresh_token(refresh_token)
    user = get_user(user_id)
    user["access_token"] = token
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing refresh token")
    return user


@user_router.get("/api/users/protected")
def protected(user_id: str = Depends(auth_handler.auth_wrapper)):
    return {"user_id": user_id}


@user_router.post("/api/users/employee", response_model=AuthResponse)
def employee_create(user_data: EmployeeCreate, response: Response):
    if not account_exists(user_data):
        employee_obj, error = create_employee(user_data)
        if error:
            raise HTTPException(status_code=409, detail=error)
        access_token, refresh_token = auth_handler.generate_tokens(employee_obj.get("id"))
        del employee_obj["id"]
        employee_obj["access_token"] = access_token
        response.set_cookie(key="refresh_token", value=refresh_token, secure=True, httponly=True, domain=".koyeb.app", path="/api", samesite="none")

        return employee_obj
    else:
        raise HTTPException(status_code=409, detail="User with this email already exists")


@user_router.post("/api/users/login", response_model=AuthResponse)
def user_login(user_data: UserLogin, response: Response):
    login_obj, error = login_user(user_data)
    if error:
        raise HTTPException(status_code=409, detail=error)
    else:
        access_token, refresh_token = auth_handler.generate_tokens(login_obj.get("id"))
        del login_obj["id"]
        login_obj["access_token"] = access_token
        response.set_cookie(key="refresh_token", value=refresh_token, secure=True, httponly=True, domain=".koyeb.app", path="/api", samesite="none")

    return login_obj


@user_router.get("/api/users/logout")
def user_logout(response: Response):
    response.set_cookie(key="refresh_token", value="", secure=True, httponly=True, domain=".koyeb.app", path="/api", samesite="none")
    return {"detail": "Logged out"}


@user_router.put("/api/users/reset_password")
def password_reset(password_data: PasswordReset):
    response, error = reset_password(password_data)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return {"detail": "Password reset successful"}


@user_router.post("/api/users/password_reset_token")
def password_reset_token(email: str):
    response, error = create_password_reset_token(email)
    if error:
        raise HTTPException(status_code=500, detail=error)
    return {"detail": "Password reset request successful"}