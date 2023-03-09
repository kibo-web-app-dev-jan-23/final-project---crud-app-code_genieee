from sqlalchemy import select, delete, create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Admin, Instructors ,Base
import random
import string

def generate_random_password():
    # get random password of length 8 with letters, digits, and symbols
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(12))
    return password



class SchoolManagementDB():
    # set logging=True to log all SQL queries
    def __init__(self, path="sqlite:///database.db", logging=False):
        self.engine = create_engine(path, echo=logging)
        Session = sessionmaker(self.engine)
        self.session = Session()
        
    def initialize_data(self, username, paswword):
        self.session.add(Admin(username=username, password=paswword))  
        self.session.commit() 

    def initialize_db_schema(self):
        Base.metadata.create_all(self.engine)
    
        
    def add_student(self, firstname, lastname, email,password, birthdate, address, year):
        self.session.add(Student(first_name = firstname,
                                 last_name = lastname,
                                 email_id = email,
                                 password = password,
                                 dateOfBirth = birthdate,
                                 address = address,
                                 current_year = year))
        self.session.commit()
        
    
        
    def get_student_info(self, email):
        return self.session.query(Student).filter_by(email_id=email).first()
    
    def view_student_in_a_class(self, student_year):
        return self.session.query(Student).filter_by(current_year=student_year).all()
    
    
    def lookup_student(self, name_to_lookup, student_year):
        result =  self.session.query(Student).filter((Student.first_name.ilike("%" + name_to_lookup + "%")
                                                                  or Student.last_name.ilike("%" + name_to_lookup + "%")),
                                                                  Student.current_year == student_year).all()
        return result
           
    
        
    def get_admin_info(self, username):
        return self.session.query(Admin).filter_by(username=username).first()
    
    def query_db(self, id):
        return self.session.query(Student).get(id) or self.session.query(Admin).get(id)
    
    def add_instructor(self, firstname, lastname, email, password):
        self.session.add(Instructors(
            first_name = firstname,
            last_name = lastname,
            email_id = email,
            password = password
        ))
        self.session.commit()
        
    def get_instructor_info(self, email):
        return self.session.query(Instructors).filter_by(email_id = email).first()
    
    def update_student_password(self, student_new_password):
        return self.session.query(Student).update(password = student_new_password)
    
    def get_all_instructors(self):
        return self.session.query(Instructors).all()