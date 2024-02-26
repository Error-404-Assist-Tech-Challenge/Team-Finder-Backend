from sqlalchemy.exc import SQLAlchemyError

from database.skill_categories.models import Skill_categories


def create_skill_categories(session, dept_id, name, created_at, skill_categories_id):
    try:
        obj = Skill_categories(dept_id=dept_id, name=name, created_at=created_at, id=skill_categories_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_skill_categories(session):
    try:
        skill_categories = session.query(Skill_categories).all()
        return Skill_categories.serialize_skill_categories(skill_categories)
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
        return error
