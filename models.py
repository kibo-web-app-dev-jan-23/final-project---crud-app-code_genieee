from sqlalchemy import String, Integer, Column, ForeignKey, Date, create_engine
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name= Column(String(50))
    username = Column(String(length=60), unique=True, nullable=False)
    email_id= Column(EmailType(), unique= True, nullable=False)
    password = Column(String(length=60), unique=True, nullable=False)
    dateOfBirth = Column(Date())
    address = Column(String())
    # year = Column(Integer)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key= True)
    name = Column(String(50))
    year_taken = Column(Integer)
    
class Instructors(Base):
    __tablename__ ="instructors"
    id = Column(Integer, primary_key= True)
    first_name = Column(String(50))
    last_name= Column(String(50))
    email_id= Column(EmailType(), unique= True)
    password = Column(String(length=60), unique=True)
    address = Column(String())

# class Year1(Base):
#     __tablename__ = "year1"
#     student_id = Column(Integer, ForeignKey("students.id"), primary_key=True) 
#     student_year = relationship("Student", back_populates="year")
    
# class Year2(Base):
#     __tablename__ = "year1"
#     Student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
#     student_year = relationship("Student", back_populates="year")
    
# class Year3(Base):
#     __tablename__ = "year1"
#     Student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
#     student_year = relationship("Student", back_populates="year")

