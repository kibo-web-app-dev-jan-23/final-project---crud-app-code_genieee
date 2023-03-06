from sqlalchemy import select, delete, create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Admin, Base



class SchoolManagementDB():
    # set logging=True to log all SQL queries
    def __init__(self, path="sqlite:///courses.db", logging=False):
        self.engine = create_engine(path, echo=logging)
        Session = sessionmaker(self.engine)
        self.session = Session()
        
    def initialize_data(self, username, paswword):
        self.session.add(Admin(username=username, password=paswword))  
        self.session.commit() 

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
        
    def get_student_info_on_login(self, username):
        return self.session.query(Student).filter_by(username=username).first() or self.session.query(Student).filter_by(email_id=username).first()
    
    def lookup_student(self, student_id_to_lookup):
        result = self.session.get(Student, student_id_to_lookup)
        if result == None:
            return f"No student with ID {student_id_to_lookup}."
        return result
    
    def search_students_by_name(self, name_to_lookup):
        return (
            self.session.query(Student)
            .filter(Student.first_name.ilike("%" + name_to_lookup + "%"))
            .all() 
            or 
            self.session.query(Student)
            .filter(Student.last_name.ilike("%" + name_to_lookup + "%"))
            .all()
        )
    
        
    def get_admin_info(self, username):
        return self.session.query(Admin).filter_by(username=username).first()
    
    def query_db(self, id):
        return self.session.query(Student).get(id) or self.session.query(Admin).get(id)
