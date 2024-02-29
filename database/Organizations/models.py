import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


#ORGANIZATIONS
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    hq_address = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    @staticmethod
    def serialize_organization(organization):
        return {
            "name": str(organization.name),
            "hq_address": str(organization.hq_address)
        }

    @staticmethod
    def serialize_organizations(organizations):
        serialize_organization = {}
        for organization in organizations:
            serialize_organization[str(organization.id)] = {
                "id": str(organization.id),
                "name": str(organization.name),
                "hq_address": str(organization.hq_address),
                "created_at": str(organization.created_at)
            }
        return serialize_organization


#ORGANIZATION_ROLES
class Organization_roles(Base):
    __tablename__ = "organization_roles"

    id = Column(UUID, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    @staticmethod
    def serialize_organization_roles(organization_roles):
        serialize_organization_roles = {}
        for organization_role in organization_roles:
            serialize_organization_roles[str(organization_role.id)] = {
                "id": str(organization_role.id),
                "name": str(organization_role.name)
            }
        return serialize_organization_roles


#USER_ROLES
class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("organization_roles.id"), primary_key=True, nullable=False)

    @staticmethod
    def serialize_user_roles(user_roles):
        serialized_user_roles = []
        for user_role in user_roles:
            serialized_user_roles.append({
                "user_id": str(user_role.user_id),
                "role_id": str(user_role.role_id)
            })
        return serialized_user_roles

#TEAM_ROLES
class TeamRoles(Base):
    __tablename__ = "team_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)

    @staticmethod
    def serialize_team_roles(team_roles):
        serialized_team_roles = {}
        for team_role in team_roles:
            serialized_team_roles[str(team_role.id)] = {
                "org_id": str(team_role.org_id),
                "name": str(team_role.name)
            }
        return serialized_team_roles


#SIGNUP_TOKENS
class SignUpTokens(Base):
    __tablename__ = "signup_tokens"

    id = Column(String, primary_key=True, nullable=False)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "expires_at": self.expires_at
        }

    @staticmethod
    def serialize_tokens(tokens):
        serialized_tokens = {}
        for token in tokens:
            serialized_tokens[str(token.id)] = {
                "org_id": str(token.org_id),
                "expires_at": str(token.expires_at)
            }

        return serialized_tokens
