from sqlalchemy.exc import SQLAlchemyError
from database.Skills.models import *

# SKILLS


def create_skill(session, category_id, name, description, skill_id, created_at, author_id, org_id):
    try:
        obj = Skill(category_id=category_id,
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
        skills = session.query(Skill).all()
        return Skill.serialize_skills(skills)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_skill(session, skill_id):
    try:
        skill = session.query(Skill).filter(Skill.id == skill_id).first()
        return skill.serialize()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def create_skill_endorsement(session, endo_id, org_id, skill_id, description, endo, proj_id, type, user_id):
    try:
        obj = Endorsements(id=endo_id, org_id=org_id, skill_id=skill_id, user_id=user_id, description=description, endo=endo, proj_id=proj_id, type=type)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_endorsements(session):
    try:
        all_endorsements = session.query(Endorsements).all()
        return Endorsements.serialize_endorsements(all_endorsements)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def delete_single_skill_endorsement(session, user_id, org_id, skill_id):
    try:
        all_endorsements = session.query(Endorsements).filter(Endorsements.user_id == user_id,
                                                              Endorsements.skill_id == skill_id).all()
        for endo in all_endorsements:
            session.delete(endo)
            session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

# USER_SKILLS


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

# SKILL PROPOSALS


def propose_skill(session, user_id, skill_id, dept_id, level, experience, proposal, id, read, for_employee = None):
    try:
        obj = Skill_proposals(user_id=user_id,
                              id=id,
                              skill_id=skill_id,
                              level=level,
                              experience=experience,
                              dept_id=dept_id,
                              proposal=proposal,
                              for_employee=for_employee,
                              read=read)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_proposed_employee_skills(session, user_id):
    try:
        skill_proposals = session.query(Skill_proposals).filter(Skill_proposals.user_id == user_id).all()
        return Skill_proposals.serialize_skill_proposals(skill_proposals)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def accept_employee_skill_proposal(session, proposal_id, level, experience):
    try:
        skill_proposal = session.query(Skill_proposals).filter(Skill_proposals.id == proposal_id).first()
        if skill_proposal:
            skill_proposal.for_employee = False
            skill_proposal.level = level
            skill_proposal.experience = experience
            session.commit()
            return skill_proposal
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def delete_employee_skill_proposal(session, proposal_id):
    try:
        skill_proposal = session.query(Skill_proposals).filter(Skill_proposals.id == proposal_id).first()
        if skill_proposal:
            session.delete(skill_proposal)
            session.commit()
            return skill_proposal
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_proposed_skills(session):
    try:
        skill_proposals = session.query(Skill_proposals).all()
        return Skill_proposals.serialize_skill_proposals(skill_proposals)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def delete_proposed_skill(session, user_id, skill_id):
    try:
        proposed_skill = session.query(Skill_proposals).filter(Skill_proposals.user_id == user_id,
                                                               Skill_proposals.skill_id == skill_id).first()
        if proposed_skill:
            session.delete(proposed_skill)
            session.commit()
            return proposed_skill
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def create_project_assignment_proposal(session, dept_id, id, assignment_id, read, user_id, role_ids, comment, proposal, dealloc_reason = None, deallocated = None):
    try:
        obj = Skill_proposals(user_id=user_id,
                              assignment_id=assignment_id,
                              role_ids=role_ids,
                              comment=comment,
                              proposal=proposal,
                              deallocated=deallocated,
                              dealloc_reason=dealloc_reason,
                              dept_id=dept_id,
                              id=id,
                              read=read)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def read_notification(session, proposal_id):
    try:
        proposed_skill = session.query(Skill_proposals).filter(Skill_proposals.id == proposal_id).first()
        if proposed_skill:
            proposed_skill.read = True
            session.commit()
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


# DEPARTMENT_SKILLS

def create_department_skill(session, dept_id, skill_id, id):
    try:
        obj = Department_skills(dept_id=dept_id, skill_id=skill_id, id=id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_all_department_skills(session):
    try:
        department_skill = session.query(Department_skills).all()
        return Department_skills.serialize_department_skills(department_skill)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_department_skills(session, dept_id):
    try:
        department_skill = session.query(Department_skills).filter(Department_skills.dept_id == dept_id).all()
        return Department_skills.serialize_department_skills(department_skill)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def get_department_skills(session, dept_id):
    try:
        department_skill = session.query(Department_skills).filter(Department_skills.dept_id == dept_id).all()
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

def delete_department_skills(session, dept_id):
    try:
        department_skills = session.query(Department_skills).filter(Department_skills.dept_id == dept_id).all()
        if department_skills:
            for skill in department_skills:
                session.delete(skill)
                session.commit()
            return department_skills
        else:
            return None
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def delete_department_skill(session, id):
    try:
        department_skill = session.query(Department_skills).filter(Department_skills.id == id).first()
        session.delete(department_skill)
        session.commit()
        return department_skill
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error

#SKILL_CATEGORIES

def create_skill_category(session, org_id, name, created_at, skill_category_id):
    try:
        obj = Skill_categories(org_id=org_id, name=name, created_at=created_at, id=skill_category_id)
        session.add(obj)
        return obj
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error


def delete_skill_category(session, skill_category_id):
    try:
        skill_category = session.query(Skill_categories).filter(Skill_categories.id == skill_category_id).first()
        if skill_category:
            session.delete(skill_category)
            return skill_category
        else:
            return None
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

