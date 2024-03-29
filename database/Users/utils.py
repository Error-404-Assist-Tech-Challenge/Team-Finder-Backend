from sqlalchemy.exc import SQLAlchemyError
from database.Users.models import Users


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
