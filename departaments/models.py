from pydantic import BaseModel


class Departament(BaseModel):
    org_id: str
    name: str
    manager_id: str
