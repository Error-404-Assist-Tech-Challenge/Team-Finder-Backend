from database.db import db


def get_organization_contacts(user_id):
    user_data = db.get_user(user_id)
    organization_id = user_data.get("org_id")

    organization_contacts, error = db.get_organization_contacts(organization_id)
    if organization_contacts:
        org_roles = db.get_organization_roles()

        for contact in organization_contacts:
            contact_org_roles = db.user_roles_get(contact.get("id"))

            user_role_names = []
            for role_id in contact_org_roles:
                if org_roles.get(role_id):
                    user_role_names.append(org_roles.get(role_id).get("name"))

            contact["roles"] = user_role_names

        return organization_contacts, None
    else:
        return None, error