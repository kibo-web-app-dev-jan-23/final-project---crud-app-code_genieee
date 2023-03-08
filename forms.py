from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField, SubmitField, IntegerField, RadioField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
# Student signup form 
class Add_student(FlaskForm):
    firstName = StringField("Firstname", validators=[InputRequired()])
    lastName = StringField("Lastname", validators= [InputRequired()])
    email = StringField("Email-Id", validators=[InputRequired(), Email(message="Input a valid email address")])
    dateOfBirth = DateField("Date-of-birth", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    year = IntegerField("Year", validators=[InputRequired(), NumberRange(min=1, max=3)])
    


#Login form    
class Login(FlaskForm):
    username = StringField("Username/email", validators=[InputRequired(), Email(message="Input a valid form")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])

#Admin login form    
class AdminLogin(FlaskForm):
    username = StringField("Username", validators=[InputRequired()], default="Admin")
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)], default="Admin200")
    
    
class AddInstructor(FlaskForm):
    firstName = StringField("Firstname", validators=[InputRequired()])
    lastName = StringField("Lastname", validators= [InputRequired()])
    email = EmailField("Email-Id", validators=[InputRequired(), Email(message="Input a valid email address")])
    
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm New Password', validators=[InputRequired()])
    submit = SubmitField('Change Password')  
    
class ViewClass(FlaskForm):
      select_year = RadioField('Select Year', choices=['Year 1', 'Year 2', 'Year 3'], validators=[InputRequired()])
      
      
#Get data from signup page    
def get_data_from_form(form):
    firstname = form.firstName.data
    lastname = form.lastName.data
    email = form.email.data
    dateOfBirth = form.dateOfBirth.data
    address = form.address.data
    year = form.year.data
    return firstname, lastname, email, dateOfBirth, address, year

def get_data_from_login_form(form):
    username = form.username.data
    password = form.password.data
    return (username, password)