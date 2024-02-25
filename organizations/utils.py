from uuid import uuid4
from database.db import db


def get_organizations():
    organizations = db.get_organizations()
    return organizations


def create_organization(data):
    organization_data = data.model_dump()
    organization_id = str(uuid4())
    organization_data["id"] = organization_id

    db.create_organization(name=organization_data.get("name"),
                           admin_id=organization_data.get("admin_id"),
                           hq_address=organization_data.get("hq_address"),
                           organization_id=organization_id)

    return organization_data
