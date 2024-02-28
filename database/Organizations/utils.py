from sqlalchemy.exc import SQLAlchemyError

from database.Organizations.models import *


#ORGANIZATION_ROLES
def create_organization_role(session, id, name):
    try:
        obj = Organization_roles(id=id, name=name)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_organization_roles(session):
    try:
        roles = session.query(Organization_roles).all()
        return Organization_roles.serialize_organization_roles(roles)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


#ORGANIZATIONS
def create_organization(session, name, hq_address, created_at, organization_id):
    try:
        obj = Organization(name=name, hq_address=hq_address, created_at=created_at, id=organization_id)
        session.add(obj)
        return obj
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



#USER_ROLES
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


#TEAM_ROLES
def create_team_role(session, id, name, org_id):
    try:
        obj = TeamRoles(id=id, name=name, org_id=org_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

def get_team_roles(session):
    try:
        team_roles = session.query(TeamRoles).all()
        return TeamRoles.serialize_team_roles(team_roles)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


#SIGNUP_TOKENS
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
