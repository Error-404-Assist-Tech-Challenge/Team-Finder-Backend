from sqlalchemy.exc import SQLAlchemyError
from database.user_skills.models import UserSkills


def create_user_skills(session, user_id, skill_id, level, experience, created_at):
    try:
        obj = UserSkills(user_id=user_id, skill_id=skill_id, level=level, experience=experience, created_at=created_at)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_user_skills(session):
    try:
        user_skills = session.query(UserSkills).all()
        return UserSkills.serialize_user_skills(user_skills)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error



def update_user_skill(session, user_id, level, experience, skill_id):
    try:
        user_skill = session.query(UserSkills).filter(UserSkills.user_id == user_id, UserSkills.skill_id == skill_id).first()
        if user_skill:
            user_skill.level = level
            user_skill.experience = experience
            session.commit()
            return user_skill
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error
