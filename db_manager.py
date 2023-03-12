from sqlalchemy import select, delete, create_engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from models import Student, Admin, Instructors, Base
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
        
    def initialize_data(self):
        # Generate hashed password from user's input password
        password = bcrypt.generate_password_hash("Admin200").decode('utf-8')
        self.session.add(Admin(username="Admin", password=paswword))  
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
        
        
    def add_instructor(self, firstname, lastname, email, password):
        self.session.add(Instructors(
            first_name = firstname,
            last_name = lastname,
            email_id = email,
            password = password
        ))
        self.session.commit()
        
        
    
        
    def get_info(self, table, email):
        return self.session.query(table).filter_by(email_id=email).first()
    
    def view_student_in_a_class(self, student_year):
        return self.session.query(Student).filter_by(current_year=student_year).all()
    
    
    def lookup(self, table, first_name, last_name):
        result =  self.session.query(table).filter(table.first_name.ilike("%" + first_name + "%"), table.last_name.ilike("%" + last_name + "%")).all()
        return result
    
    
    
        
    def get_admin_info(self, username):
        return self.session.query(Admin).filter_by(username=username).first()
    
    def query_db(self, id):
        return self.session.query(Student).get(id) or self.session.query(Admin).get(id) or self.session.query(Instructors).get(id)
    
    
    def update_password(self, table, new_password):
        self.session.query(table).update({table.password:new_password})
        self.session.commit()
    
    def get_all_instructors(self):
        return self.session.query(Instructors).all()
    
    def delete_info(self, user):
        self.session.delete(user)
        self.session.commit()
