from uuid import uuid4
from database.db import db


def get_organization_members():
    members = db.get_organization_members()
    return members


def create_organization_member(data):
    organization_member_data = data.model_dump()
    organization_member_id = str(uuid4())
    organization_member_data["id"] = organization_member_id

    db.create_organization_member(org_id=organization_member_data.get("org_id"),
                                  user_id=organization_member_data.get("user_id"),
                                  organization_member_id=organization_member_id)
    return organization_member_data
