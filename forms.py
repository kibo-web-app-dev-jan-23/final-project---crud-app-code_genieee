# Import necessary modules for form creation and validation
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField, SubmitField, IntegerField, RadioField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from wtforms import StringField, PasswordField, EmailField, DateField, SubmitField
from wtforms.validators import InputRequired, Length, Email, DataRequired, EqualTo

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
    
# Define a form for adding an instructor   
class AddInstructor(FlaskForm):
    firstName = StringField("Firstname", validators=[InputRequired()])
    lastName = StringField("Lastname", validators= [InputRequired()])
    email = EmailField("Email-Id", validators=[InputRequired(), Email(message="Input a valid email address")])

# Define a form for changing user password
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm New Password', validators=[InputRequired()])

# Define a form for selecting a class    
class ViewClass(FlaskForm):
    select_year = RadioField('Select Year', choices=['Year 1', 'Year 2', 'Year 3'], validators=[InputRequired()])

# Define a form for searching user information      
class SearchInfo(FlaskForm):
    first_name = StringField('FirstName', validators=[InputRequired()])
    last_name = StringField('LastName', validators=[InputRequired()])


# Define a form for deleting user information
class DeleteInfo(FlaskForm):
    email = StringField("Email-Id", validators=[InputRequired(), Email(message="Input a valid email address")])
      
      
    

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