from sqlalchemy import select, delete, create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Base


class SchoolManagementDB():
    # set logging=True to log all SQL queries
    def __init__(self, path="sqlite:///courses.db", logging=False):
        self.engine = create_engine(path, echo=logging)
        Session = sessionmaker(self.engine)
        self.session = Session()

    def initialize_db_schema(self):
        Base.metadata.create_all(self.engine)
        
    def add_student(self, firstname, lastname, username, email, password, birthdate, address):
        self.session.add(Student(first_name = firstname,
                                 last_name = lastname,
                                 username = username,
                                 email_id = email,
                                 password = password,
                                 dateOfBirth = birthdate,
                                 address = address,))
        self.session.commit()