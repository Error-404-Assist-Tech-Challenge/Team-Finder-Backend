from sqlalchemy.exc import SQLAlchemyError
from database.user_skills.models import UserSkills


def create_user_skills(session, user_id, skill_id, level, experience, created_at):
    try:
        obj = UserSkills(user_id=user_id, skill_id=skill_id, level=level, experience=experience, created_at=created_at)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_user_skills(session):
    try:
        user_roles = session.query(UserSkills).all()
        return UserSkills.serialize_user_skills(user_roles)
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
        return error
