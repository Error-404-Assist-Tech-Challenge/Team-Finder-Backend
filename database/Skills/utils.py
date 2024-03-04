from sqlalchemy.exc import SQLAlchemyError
from database.Skills.models import *

#SKILLS

def create_skill(session, category_id, name, description, skill_id, created_at, author_id, org_id):
    try:
        obj = Skills(category_id=category_id,
                     name=name,
                     description=description,
                     created_at=created_at,
                     author_id=author_id,
                     org_id=org_id,
                     id=skill_id)
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_skills(session):
    try:
        skills = session.query(Skills).all()
        return Skills.serialize_skills(skills)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

#USER_SKILLS

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

def remove_user_skill(session, user_id, skill_id):
    try:
        user_skill = session.query(UserSkills).filter(UserSkills.user_id == user_id, UserSkills.skill_id == skill_id).first()
        if user_skill:
            session.delete(user_skill)
            session.commit()
            return user_skill
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


#DEPARTMENT_SKILLS
def create_department_skill(session, dept_id, skill_id):
    try:
        obj = Department_skills(dept_id=dept_id, skill_id=skill_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_department_skills(session):
    try:
        department_skill = session.query(Department_skills).all()
        return Department_skills.serialize_department_skills(department_skill)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

def update_department_skill(session, dept_id, skill_id, new_dept_id, new_skill_id):
    try:
        department_skill = session.query(Department_skills).filter(
            Department_skills.dept_id == dept_id,
            Department_skills.skill_id == skill_id
        ).first()

        if department_skill:
            if dept_id != new_dept_id:
                department_skill.dept_id = new_dept_id
            if skill_id != new_skill_id:
                department_skill.skill_id = new_skill_id

            session.commit()
            return department_skill
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        session.rollback()
        print(error)
        return error




#SKILL_CATEGORIES

def create_skill_categories(session, org_id, name, created_at, skill_categories_id):
    try:
        obj = Skill_categories(org_id=org_id, name=name, created_at=created_at, id=skill_categories_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_skill_categories(session):
    try:
        skill_categories = session.query(Skill_categories).all()
        return Skill_categories.serialize_skill_categories(skill_categories)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

def update_skill_category(session, id, org_id, name, modified_at):
    try:
        skill_category = session.query(Skill_categories).filter(Skill_categories.id == id).first()
        if skill_category:
            skill_category.org_id = org_id
            skill_category.name = name
            skill_category.created_at = modified_at
            session.commit()
            return skill_category
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

