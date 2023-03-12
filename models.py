from sqlalchemy import String, Integer, Column, ForeignKey, Date
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship, declarative_base
from flask_login import UserMixin


# Declare the base class for declarative models
Base = declarative_base()


# Define the Student model for database table 'students
class Student(UserMixin, Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True) # primary key column
    first_name = Column(String(50)) # student's first name column
    last_name= Column(String(50))  # student's last name column
    email_id= Column(EmailType(), unique= True, nullable=False) # student's email id column
    password = Column(String(length=60), nullable=False) # hashed password column
    dateOfBirth = Column(Date()) # student's date of birth column
    address = Column(String()) # student's address column
    current_year = Column(Integer) # student's current year of study column


# Define the Instructors model for database table 'instructors'       
class Instructors(UserMixin, Base):
    __tablename__ ="instructors"
    id = Column(Integer, primary_key= True) # primary key column
    first_name = Column(String(50))  # instructor's first name column
    last_name= Column(String(50))  # instructor's last name column
    email_id= Column(EmailType(), unique= True)  # instructor's email id column
    password = Column(String(length=60), nullable=False) # hashed password column
   


# Define the Admin model for database table 'admin'
class Admin(UserMixin, Base):
    __tablename__ ="admin"
    id = Column(Integer, primary_key= True)  # primary key column
    username = Column(String(50), unique=True)  # admin's username column
    password = Column(String(length=60), unique=True)  # hashed password column
 
    
   
