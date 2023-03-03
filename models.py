from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name= Column(String(50))
    email_id= Column(EmailType())
    password = Column(String(length=60))
    dateOfBirth = Column()
    courses = relationship("Enrollment", back_populates="student")

    def __repr__(self):
        return f"enrolled in {self.course.name}"