from sqlalchemy.exc import SQLAlchemyError

from database.skills.models import Skills


def create_skill(session, dept_id, category_id, name, description, skill_id, created_at):
    try:
        obj = Skills(dept_id=dept_id, category_id=category_id, name=name, description=description, created_at=created_at, id=skill_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_skills(session):
    try:
        skills = session.query(Skills).all()
        return Skills.serialize_skills(skills)
    except SQLAlchemyError as e:
        session.rollback()
        error = str(e.__dict__['orig'])
        print(error)
        return error
