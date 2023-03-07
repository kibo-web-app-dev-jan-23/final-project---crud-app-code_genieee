from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField, SubmitField
from wtforms.validators import InputRequired, Length, Email, DataRequired, EqualTo
# Student signup form 
class Add_student(FlaskForm):
    firstName = StringField("Firstname", validators=[InputRequired()])
    lastName = StringField("Lastname", validators= [InputRequired()])
    email = EmailField("Email-Id", validators=[InputRequired(), Email(message="Input a valid email address")])
    dateOfBirth = DateField("Date-of-birth", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])


#Login form    
class Login(FlaskForm):
    username = StringField("Username/email", validators=[InputRequired(), Email(message="Input a valid form")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])

#Admin login form    
class AdminLogin(FlaskForm):
    username = StringField("email_id", validators=[InputRequired()], default="Admin")
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)], default="Admin200")
    
    
class AddInstructor(FlaskForm):
    firstName = StringField("Firstname", validators=[InputRequired()])
    lastName = StringField("Lastname", validators= [InputRequired()])
    email = EmailField("Email-Id", validators=[InputRequired(), Email(message="Input a valid email address")])

#student to change password
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')    

#Get data from signup page    
def get_data_from_form(form):
    firstname = form.firstName.data
    lastname = form.lastName.data
    email = form.email.data
    dateOfBirth = form.dateOfBirth.data
    address = form.address.data
    return firstname, lastname, email, dateOfBirth, address

def get_data_from_login_form(form):
    username = form.username.data
    password = form.password.data
    return (username, password)