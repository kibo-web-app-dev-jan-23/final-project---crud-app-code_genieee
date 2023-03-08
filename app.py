from flask import Flask, render_template, redirect, url_for, flash
from db_manager import SchoolManagementDB, generate_random_password
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from forms import Add_student, AddInstructor, Login, AdminLogin, ChangePasswordForm, ViewClass, get_data_from_form, get_data_from_login_form
from wtforms.validators import ValidationError
from pyisemail import is_email
from models import Admin




app = Flask(__name__)
app.config['SECRET_KEY'] = "Don'tTellAnyone"
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)


manager = SchoolManagementDB()
manager.initialize_db_schema()



@login_manager.user_loader
def load_user(id):
    user= manager.query_db(id)
    return (user)

   
@app.route('/student_login', methods=["GET", "POST"])
def student_login():
    form = Login()
    if form.validate_on_submit():
        try:
           username, password = get_data_from_login_form(form) 
           user = manager.get_student_info(username)
           if user:
               if bcrypt.check_password_hash(user.password, password):
                #    login_user(user)
                   return f"Welcome"
        except:
            return "User does not exist"
    return render_template("student_login.html", form= form)


@app.route('/instructor_login', methods=["GET", "POST"])
def instructor_login():
    form = Login()
    if form.validate_on_submit():
        username, password = get_data_from_login_form(form)
        user = manager.get_instructor_info(username)
        if user:
            if bcrypt.check_password_hash(user.password, password):
                # login_user(user)
                return(f"Welcome {user.first_name} {user.last_name}")
    return render_template("instructors_login.html", form= form)

@app.route('/admin', methods=["GET", "POST"])
def admin_login():
    form = AdminLogin()
    password = bcrypt.generate_password_hash(form.password.default).decode('utf-8')
    if manager.get_admin_info(form.username.default)==None:
        manager.initialize_data(form.username.default, password)
        if form.validate_on_submit():
            username, password = get_data_from_login_form(form)
            user = manager.get_admin_info(username)
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
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

@app.route("/add_instructor", methods=["GET", "POST"])
@login_required
def add_instructors():
    form = AddInstructor()
    password = generate_random_password()
    secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
    if form.validate_on_submit():
        if manager.get_instructor_info(form.email.data) == None:
            manager.add_instructor(form.firstName.data, form.lastName.data, form.email.data, secure_password)
            return(f"Instructor added successfully. Instructor's password is {password}")
        else:
            return "This instructor has been registered"
    return render_template("instructor.html", form=form)

@app.route("/view_class", methods=["GET", "POST"])
@login_required
def view_class():
    form = ViewClass()
    if form.validate_on_submit():
        if form.select_year.data == "Year 1":
            result = manager.view_student_in_a_class(1)
        elif form.select_year.data == "Year 2":
            result = manager.view_student_in_a_class(2)
        elif form.select_year.data == "Year 3":
            result = manager.view_student_in_a_class(3)
        return render_template("student.html", result=result)    
    return render_template("view_class.html", form = form)

@app.route('/add_student', methods=["GET", "POST"])
@login_required
def add_student():
    form = Add_student()
    password = generate_random_password()
    secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
    firstname,lastname,email,dob,address,year = get_data_from_form(form)
    if form.validate_on_submit():
        if is_email(email, check_dns=True) == False:
            flash("Email does not exist", "error")
            redirect("/add_student")
        else:
            check_student = manager.get_student_info(email)
            if check_student == None:
                manager.add_student(firstname,lastname,email,secure_password,dob,address, year)
                flash (f"Student added successfully. Student password is {password}", "success")
                redirect("/add_student")
            else:
                flash ("The email you entered has been used by a student", "error")
                return redirect("/add_student")
    return render_template("add_student.html", form= form)

@app.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_student_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        manager.update_student_password(form.new_password)
        flash('Your password has been changed.', 'success')
        return redirect(url_for('student_login'))
    else:
        flash('Invalid password.', 'error')
    return render_template('change_password.html', form=form)

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def log_out():
    logout_user()
    return redirect("/admin")


        
        