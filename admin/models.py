from pydantic import BaseModel

class OrganizationAdmin(BaseModel):
    name: str
    email: str
    password: str
    oname : str
    address : str
