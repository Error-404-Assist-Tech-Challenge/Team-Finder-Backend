from uuid import UUID
from pydantic import BaseModel


class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    org_name: str
    hq_address: str
    org_id: str


class AuthResponse(BaseModel):
    id: UUID
    name: str
    email: str
    password: str
    org_id: UUID
    token: str


class EmployeeCreate(BaseModel):
    name: str
    email: str
    password: str
    org_id: UUID


class UserLogin(BaseModel):
    email: str
    password: str
