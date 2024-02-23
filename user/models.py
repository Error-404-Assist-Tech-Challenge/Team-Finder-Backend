from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    org_name: str
    hq_address: str