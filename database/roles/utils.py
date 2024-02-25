from database.roles.models import Role


def get_roles(session):
    roles = session.query(Role).all()
    return Role.serialize_roles(roles)
