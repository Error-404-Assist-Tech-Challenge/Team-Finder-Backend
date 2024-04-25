from sqlalchemy.exc import SQLAlchemyError
from database.Messages.models import Messages


def create_message(session, id, user_id, value, discussion_id, created_at):
    try:
        obj = Messages(id=id,
                       user_id=user_id,
                       value=value,
                       discussion_id=discussion_id,
                       created_at=created_at)
        session.add(obj)
        return obj.serialize(), None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error


def get_messages(session):
    try:
        messages = session.query(Messages).all()
        if messages:
            return Messages.serialize_messages(messages), None
        else:
            return {}, "No messages found"
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error
