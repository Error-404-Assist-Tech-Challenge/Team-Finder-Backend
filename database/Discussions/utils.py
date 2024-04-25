from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import session
from database.Discussions.models import Discussions
from sqlalchemy import func


def get_user_discussions(session, user_id):
    try:
        discussions = session.query(Discussions).filter(Discussions.contacts.any(user_id)).all()
        if discussions:
            return discussions, None
        else:
            return [], {"error_message: 'No discussions found'"}
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error


def get_discussions(session):
    try:
        companies = session.query(Discussions).all()
        if companies:
            return Discussions.serialize_discussions(companies), None
        else:
            return [], {"error_message: 'No discussions found'"}
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error


def create_discussion(session, contacts, discussion_id, name):
    try:
        obj = Discussions(contacts=contacts, id=discussion_id, name=name)
        session.add(obj)
        return obj.serialize(), None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error
