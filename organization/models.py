from pydantic import BaseModel


class Organization(BaseModel):
    admin_id: str
    name: str
    hq_address: str
