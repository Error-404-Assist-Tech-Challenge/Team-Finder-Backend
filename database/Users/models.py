import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    def serialize(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "email": str(self.email),
            "password": str(self.password),
            "org_id": str(self.org_id),
            "created_at": str(self.created_at)
        }

    @staticmethod
    def serialize_users(users):
        serialized_users = {}
        for user in users:
            serialized_users[str(user.id)] = {
                "id": str(user.id),
                "name": str(user.name),
                "email": str(user.email),
                "password": str(user.password),
                "org_id": str(user.org_id),
                "created_at": str(user.created_at)
            }
        return serialized_users


# PASSWORD_RESET_TOKEN
class PasswordResetTokens(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "expires_at": self.expires_at
        }

    @staticmethod
    def serialize_tokens(tokens):
        serialized_tokens = []
        for token in tokens:
            serialized_tokens.append({
                "id": str(token.id),
                "user_id": str(token.user_id),
                "expires_at": str(token.expires_at)
            })

        return serialized_tokens
