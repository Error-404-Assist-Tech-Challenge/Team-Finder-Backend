from sqlalchemy.exc import SQLAlchemyError
from database.Users.models import Users, PasswordResetTokens


def create_user(session, name, email, password, user_id, created_at, org_id):
    try:
        obj = Users(name=name, email=email, password=password, id=user_id, created_at=created_at, org_id=org_id)
        session.add(obj)
        return obj.serialize(), None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error


def get_users(session):
    try:
        users = session.query(Users).all()
        return Users.serialize_users(users)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return []


def get_user(session, id):
    try:
        user = session.query(Users).filter_by(id=id).first()
        return user.serialize()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return []


# PASSWORD_RESET_TOKEN
def create_password_reset_token(session, id, user_id, expires_at):
    try:
        token = PasswordResetTokens(id=id, user_id=user_id, expires_at=expires_at)
        session.add(token)
        return token.serialize(), None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error


def get_password_reset_tokens(session):
    try:
        tokens = session.query(PasswordResetTokens).all()
        return PasswordResetTokens.serialize_tokens(tokens)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return []


def delete_password_reset_tokens(session, id):
    try:
        token = session.query(PasswordResetTokens).filter_by(id=id).first()
        if token:
            session.delete(token)
        else:
            return None, "Token not found"
        return "Token deleted", None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error
