from uuid import UUID
from pydantic import BaseModel
from typing import List, Literal


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
    organization_status: Literal['paid', 'unpaid', 'demo']


class EmployeeCreate(BaseModel):
    name: str
    email: str
    password: str
    token: str


class UserLogin(BaseModel):
    email: str
    password: str


class PasswordReset(BaseModel):
    token: str
    password: str
