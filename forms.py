from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField
from wtforms.validators import InputRequired, Length, Email
from db_manager import SchoolManagementDB


app = Flask(__name__)
app.config['SECRET_KEY'] = "Don'tTellAnyone"

manager = SchoolManagementDB()
manager.initialize_db_schema()

# Student signup form 
class Signup(FlaskForm):
    firstName = StringField("Firstname", validators=[InputRequired()])
    lastName = StringField("Lastname", validators= [InputRequired()])
    username= StringField("Username", validators=[InputRequired()])
    email = EmailField("Email-Id", validators=[InputRequired(), Email(message="Input a valid email address")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])
    dateOfBirth = DateField("Date-of-birth", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])

#instructor signup form   
class InstructorSignup(FlaskForm):
    firstName = StringField("Firstname", validators=[InputRequired()])
    lastName = StringField("Lastname", validators= [InputRequired()])
    username= StringField("Username", validators=[InputRequired()])
    email = EmailField("Email-Id", validators=[InputRequired(), Email(message="Input a valid email address")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])
    address = StringField("Address", validators=[InputRequired()])

#Login form    
class Login(FlaskForm):
    username = StringField("Username/email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])

#Admin login form    
class Admin(FlaskForm):
    username = StringField("Username/email", validators=[InputRequired()], default= "admin")
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)], default="admin200")

#Get data from signup page    
def get_data_from_signup(form):
    firstname = form.firstName.data
    lasttname = form.lastName.data
    username = form.username.data
    email = form.email.data
    password = form.password.data
    dateOfBirth = form.dateOfBirth.data
    address = form.address.data
    return (firstname, lasttname, username, email, password, dateOfBirth, address)


@app.route('/', methods=["GET", "POST"])
def student_signup():
    form = Signup()
    if form.validate_on_submit():
        data = get_data_from_signup(form)
        try:
            manager.add_student(*data)
            return("Successfully added student")
        except:
            render_template("student_signup.html", form= form)
    return render_template("student_signup.html", form= form)

@app.route('/student_login', methods=["GET", "POST"])
def student_login():
    form = Login()
    if form.validate_on_submit():
        return "Form Successfully Submitted!"
    return render_template("student_login.html", form= form)


@app.route('/instructor_signup', methods=["GET", "POST"])
def instructor_signup():
    form = InstructorSignup()
    if form.validate_on_submit():
        return "Form Successfully Submitted!"
    return render_template("instructor_signup.html", form= form)

@app.route('/instructor_login', methods=["GET", "POST"])
def instructor_login():
    form = Login()
    if form.validate_on_submit():
        return "Form Successfully Submitted!"
    return render_template("instructors_login.html", form= form)

@app.route('/admin', methods=["GET", "POST"])
def admin_login():
    form = Admin()
    if form.validate_on_submit():
        return "Form Successfully Submitted!"
    return render_template("admin.html", form= form)