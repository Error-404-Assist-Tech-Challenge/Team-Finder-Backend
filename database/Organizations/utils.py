from sqlalchemy.exc import SQLAlchemyError

from database.Organizations.models import *
from database.Skills.models import Skills

#ORGANIZATION_ROLES
def create_organization_role(session, organization_role_id, name):
    try:
        obj = Organization_roles(id=organization_role_id, name=name)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

def get_organization_roles(session):
    try:
        organization_roles = session.query(Organization_roles).all()
        return Organization_roles.serialize_organization_roles(organization_roles)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

# ORGANIZATIONS
def create_organization(session, name, hq_address, created_at, organization_id):
    try:
        obj = Organization(name=name, hq_address=hq_address, created_at=created_at, id=organization_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def update_organization_skill(session, category_id, name, description, created_at, skill_id):
    try:
        modified_skill = session.query(Skills).filter(Skills.skill_id == skill_id).first()
        if modified_skill:
            modified_skill.category_id = category_id
            modified_skill.name = name
            modified_skill.description = description
            modified_skill.created_at = created_at
            session.commit()
            return modified_skill
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_organizations(session):
    try:
        organizations = session.query(Organization).all()
        return Organization.serialize_organizations(organizations)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_organization(session, id):
    try:
        organization = session.query(Organization).filter_by(id=id).first()
        return Organization.serialize_organization(organization)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


# USER_ROLES
def create_user_role(session, user_id, role_id):
    try:
        obj = UserRole(user_id=user_id, role_id=role_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_user_roles(session, user_id):
    try:
        user_roles = session.query(UserRole).filter_by(user_id=user_id).all()
        return UserRole.serialize_user_roles(user_roles)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_all_user_roles(session):
    try:
        user_roles = session.query(UserRole).all()
        return UserRole.serialize_user_roles(user_roles)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def remove_user_role(session, user_id, role_id):
    try:
        removed_role = session.query(UserRole).filter(UserRole.user_id == user_id,
                                                      UserRole.role_id == role_id).first()
        session.delete(removed_role)
        session.commit()
        return removed_role
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error



# TEAM_ROLES
def create_team_role(session, id, name, org_id):
    try:
        obj = TeamRoles(id=id, name=name, org_id=org_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def update_team_role(session, id, name):
    try:
        team_role = session.query(TeamRoles).filter_by(id=id).first()
        if team_role:
            team_role.name = name
            return team_role
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def delete_team_role(session, id):
    try:
        team_role = session.query(TeamRoles).filter_by(id=id).first()
        if team_role:
            session.delete(team_role)
        else:
            return None, "Team role not found"
        return "Team role deleted", None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_team_roles(session, org_id):
    try:
        team_roles = session.query(TeamRoles).filter_by(org_id=org_id).all()
        return TeamRoles.serialize_team_roles(team_roles)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


# SIGNUP_TOKENS
def create_signup_token(session, id, org_id, expires_at):
    try:
        token = SignUpTokens(id=id, org_id=org_id, expires_at=expires_at)
        session.add(token)
        return token.serialize(), None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error


def delete_signup_token(session, id):
    try:
        token = session.query(SignUpTokens).filter_by(id=id).first()
        if token:
            session.delete(token)
        else:
            return None, "Token not found"
        return "Token deleted", None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error


def get_signup_tokens(session):
    try:
        tokens = session.query(SignUpTokens).all()
        return SignUpTokens.serialize_tokens(tokens)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return []


def get_org_signup_tokens(session, org_id):
    try:
        tokens = session.query(SignUpTokens).filter_by(org_id=org_id).all()
        return SignUpTokens.serialize_tokens(tokens)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return []


def get_signup_token(session, id):
    try:
        token = session.query(SignUpTokens).filter_by(id=id)
        return SignUpTokens.serialize_tokens(token)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return []
