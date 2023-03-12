from sqlalchemy import String, Integer, Column, ForeignKey, Date
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship, declarative_base
from flask_login import UserMixin




Base = declarative_base()

class Student(UserMixin, Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name= Column(String(50))
    email_id= Column(EmailType(), unique= True, nullable=False)
    password = Column(String(length=60), nullable=False)
    dateOfBirth = Column(Date())
    address = Column(String())
    current_year = Column(Integer)
       
class Instructors(UserMixin, Base):
    __tablename__ ="instructors"
    id = Column(Integer, primary_key= True)
    first_name = Column(String(50))
    last_name= Column(String(50))
    email_id= Column(EmailType(), unique= True)
    password = Column(String(length=60), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), default=3)

class Admin(UserMixin, Base):
    __tablename__ ="admin"
    id = Column(Integer, primary_key= True)
    username = Column(String(50), unique=True)
    password = Column(String(length=60), unique=True)
 
    
   
