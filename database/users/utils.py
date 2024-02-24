
from sqlalchemy.exc import SQLAlchemyError
from user.models import UserCreate

def create_user(session, name, email, password, user_id):
    try:
        obj = UserCreate(name=name, email=email, password=password, id=user_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_users(session):
    users = session.query(UserCreate).all()
    return UserCreate.serialize_employees(users)