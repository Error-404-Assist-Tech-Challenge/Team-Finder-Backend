from sqlalchemy.exc import SQLAlchemyError
from database.Discussions.models import Discussions
from database.Users.models import Users


def get_user_discussions(session, user_id):
    try:
        discussions = session.query(Discussions).filter(Discussions.contacts.any(user_id)).all()
        if discussions:
            return Discussions.serialize_discussions(discussions), None
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
        print(contacts)
        obj = Discussions(contacts=contacts, id=discussion_id, name=name)
        session.add(obj)
        return obj.serialize(), None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error


# CONTACTS
def get_organization_contacts(session, organization_id):
    try:
        contacts = session.query(Users).filter(Users.org_id == organization_id).all()
        if contacts:
            return Users.serialize_contacts(contacts), None
        else:
            return None, 'No contacts found'
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return None, error