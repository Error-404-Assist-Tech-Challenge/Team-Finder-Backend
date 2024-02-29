from uuid import UUID
from pydantic import BaseModel
from typing import List


class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    org_name: str
    hq_address: str


class AuthResponse(BaseModel):
    name: str
    email: str
    org_name: str
    hq_address: str
    roles: List[str]
    access_token: str


class EmployeeCreate(BaseModel):
    name: str
    email: str
    password: str
    token: str


class UserLogin(BaseModel):
    email: str
    password: str
