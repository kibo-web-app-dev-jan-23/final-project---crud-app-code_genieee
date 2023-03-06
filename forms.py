from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField
from wtforms.validators import InputRequired, Length, Email
from db_manager import SchoolManagementDB
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user, login_user
from models import Admin




app = Flask(__name__)
app.config['SECRET_KEY'] = "Don'tTellAnyone"
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

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


#Login form    
class Login(FlaskForm):
    username = StringField("Username/email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])

#Admin login form    
class Admin(FlaskForm):
    username = StringField("Username/email", validators=[InputRequired()], default="Admin")
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)], default="Admin200")

#Get data from signup page    
def get_data_from_signup(form):
    firstname = form.firstName.data
    lasttname = form.lastName.data
    username = form.username.data
    email = form.email.data
    password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    dateOfBirth = form.dateOfBirth.data
    address = form.address.data
    return (firstname, lasttname, username, email, password, dateOfBirth, address)

def get_data_from_login_form(form):
    username = form.username.data
    password = form.password.data
    return (username, password)

@login_manager.user_loader
def load_user(id):
    user= manager.query_db(id)
    return (user)

   
@app.route('/', methods=["GET", "POST"])
def student_signup():
    form = Signup()
    if form.validate_on_submit():
        data = get_data_from_signup(form)
        check_user = manager.get_student_info_on_login(form.username.data)
        if check_user != None:
            if form.username.data == check_user.username or form.email.data == check_user.email_id:
                flash("One of the email or username you entered has been used")
                return redirect("/")
        else:
            manager.add_student(*data)
            return redirect("/student_login")
    return render_template("student_signup.html", form= form)

@app.route('/student_login', methods=["GET", "POST"])
def student_login():
    form = Login()
    if form.validate_on_submit():
        try:
           username, password = get_data_from_login_form(form) 
           user = manager.get_student_info_on_login(username)
           if user:
               if bcrypt.check_password_hash(user.password, password):
                   login_user(user)
                   return f"Welcome {user.username}"
        except:
            return "User does not exist"
    return render_template("student_login.html", form= form)


@app.route('/instructor_login', methods=["GET", "POST"])
def instructor_login():
    form = Login()
    if form.validate_on_submit():
        return "Form Successfully Submitted!"
    return render_template("instructors_login.html", form= form)

@app.route('/admin', methods=["GET", "POST"])
def admin_login():
    form = Admin()
    password = bcrypt.generate_password_hash(form.password.default).decode('utf-8')
    if manager.get_admin_info(form.username.default)==None:
        manager.initialize_data(form.username.default, password)
        if form.validate_on_submit():
            username, password = get_data_from_login_form(form)
            user = manager.get_admin_info(username)
            if user:
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect(url_for("admin_homepage"))
                else:
                    return "Invalid password"
    else:
        if form.validate_on_submit():
            username, password = get_data_from_login_form(form)
            user = manager.get_admin_info(username)
            if user:
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect(url_for("admin_homepage"))
                else:
                    return "Invalid password"
    
    return render_template("admin.html", form= form)


@app.route("/admin_homepage", methods=["GET", "POST"])
@login_required
def admin_homepage():
    return render_template("admin_homepage.html")
        
        