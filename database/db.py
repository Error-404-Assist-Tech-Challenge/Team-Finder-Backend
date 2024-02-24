from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.config import USER, PASSWORD, HOST, PORT, DB_NAME
from database.models import Base
from database.utils import get_employees, create_employee

engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')

with engine.connect() as connection:
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)


class DataBase:
    @staticmethod
    def create_employee(name, email, password, employee_id):
        return create_employee(session=session, name=name, email=email, password=password, employee_id=employee_id)

    @staticmethod
    def get_employees():
        return get_employees(session=session)


db = DataBase()
