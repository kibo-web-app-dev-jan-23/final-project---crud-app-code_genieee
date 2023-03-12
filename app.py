from flask import Flask, render_template, redirect, url_for, flash, session
from db_manager import SchoolManagementDB, generate_random_password
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from forms import Add_student, AddInstructor, Login, AdminLogin, ChangePasswordForm, ViewClass, SearchInfo, DeleteInfo, get_data_from_form, get_data_from_login_form
from models import Student, Instructors
from pyisemail import is_email
from flask_principal import Principal, Permission, RoleNeed, UserNeed, identity_loaded
from rolebased import be_instructor, be_admin, be_student, admin, student, instructor, AdminAccessPermission





app = Flask(__name__)
app.config['SECRET_KEY'] = "Don'tTellAnyone"
app.config['USE_SESSION_FOR_NEXT'] = True
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
# principal = Principal(app)
# principal.init_app(app) 

manager = SchoolManagementDB()
manager.initialize_db_schema()
# manager.insert_roles()



@login_manager.user_loader
def load_user(id):
    user= manager.query_db(id)
    return (user)



  
# admin_permission = admin

# Routing
# Homepage route
@app.get("/")
@app.get("/home")
def homepage():
    return render_template("home.html")

   
@app.route('/student_login', methods=["GET", "POST"])
def student_login():
    form = Login()
    if form.validate_on_submit():
        username, password = get_data_from_login_form(form) 
        user = manager.get_info(Student, username)
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect("/user_page")
                   
            else:
                flash("Wrong Password", "error")
                redirect('/student_login')
        else:
            flash("User does not exist", 'error')
            return redirect("/student_login")
    return render_template("student_login.html", form= form)


@app.route('/instructor_login', methods=["GET", "POST"])
def instructor_login():
    form = Login()
    if form.validate_on_submit():
        username, password = get_data_from_login_form(form)
        user = manager.get_info(Instructors, username)
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect('/user_page')
        
            else:
                flash("Wrong Password", "error")
                redirect('/instructor_login')
        else:
            flash("User does not exist", 'error')
            return redirect("/instructor_login")
    return render_template("instructor_login.html", form= form)

@app.route('/user_page', methods=["GET", "POST"])
@login_required
def user_page():
    return render_template("homepage.html")



@app.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_student_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            new_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            manager.update_password(Student, new_password)
            flash('Your password has been changed.', 'success')
            return redirect(url_for('student_login'))
        else:
            flash('Invalid password.', 'error')
    return render_template('change_password.html', form=form)

@app.route('/logout_user', methods=['POST', 'GET'])
@login_required
def log_out():
    logout_user()
    return redirect("/home")

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
                    flash("Invalid password", "error")
                    redirect("/admin")
            else:
                flash("Invalid Username", "error")
                redirect("/admin")
    else:
        if form.validate_on_submit():
            username, password = get_data_from_login_form(form)
            user = manager.get_admin_info(username)
            if user:
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect(url_for("admin_homepage"))
                else:
                    flash("Invalid password", "error")
                    redirect("/admin")
            else:
                flash("Invalid Username", "error")
                redirect("/admin")
    return render_template("admin.html", form= form)


@app.route("/admin_homepage", methods=["GET", "POST"])
# @admin_permission.require()
@login_required
def admin_homepage():
    return render_template("admin_homepage.html")

@app.route("/add_instructor", methods=["GET", "POST"])
# @admin_permission.require()
@login_required
def add_instructors():
    form = AddInstructor()
    password = generate_random_password()
    secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
    if form.validate_on_submit():
        if is_email(form.email.data, check_dns=True) == False:
            flash("Email does not exist", "error")
            redirect("/add_instructor")
        else:
            check_instructor = manager.get_info(Instructors, form.email.data)
            if  check_instructor == None:
                manager.add_instructor(form.firstName.data, form.lastName.data, form.email.data, secure_password)
                flash(f"Instructor added successfully. Instructor's password is {password}", "success")
                return redirect("/add_instructor")
            else:
                flash("This instructor has been registered", "error")
    return render_template("instructor.html", form=form)


@app.route('/add_student', methods=["GET", "POST"])
# @admin_permission.require()
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
            check_student = manager.get_info(Student, email)
            if check_student == None:
                manager.add_student(firstname,lastname,email,secure_password,dob,address, year)
                flash (f"Student added successfully. Student password is {password}", "success")
                return redirect("/add_student")
            else:
                flash ("The email you entered has been used by a student", "error")
                redirect("/add_student")
    return render_template("add_student.html", form= form)

@app.route("/view_class", methods=["GET", "POST"])
# @admin_permission.require()
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

@app.route("/view_instructors", methods=["GET", "POST"])
# @admin_permission.require()
@login_required
def view_all_instructors():
    result = manager.get_all_instructors()
    return render_template("available_instructors.html",result=result)



@app.route('/search_student', methods=['POST', 'GET'])
# @admin_permission.require()
@login_required
def search_for_student():
    form = SearchInfo()
    if form.validate_on_submit():
        result = manager.lookup(Student, form.first_name.data, form.last_name.data)
        if result:
            return render_template("student.html", result=result)
        else:
            flash("Student does not exist", "error")
            return redirect("/search_student")
    return render_template("search.html", form=form) 

@app.route('/search_instructor', methods=['POST', 'GET'])
# @admin_permission.require()
@login_required
def search_for_instructor():
    form = SearchInfo()
    if form.validate_on_submit():
        result = manager.lookup(Instructors, form.first_name.data, form.last_name.data)
        if result:
            return render_template("available_instructor.html", result=result)
        else:
            flash("Instructor does not exist", "error")
            return redirect("/search_instructor")
    return render_template("search.html", form=form) 

@app.route('/delete_instructor', methods=['POST', 'GET'])
# @admin_permission.require()
@login_required
def delete_instructor():
    form = DeleteInfo()
    if form.validate_on_submit():
        user = manager.get_info(Instructors, form.email.data)
        if user:
            manager.delete_info(user)
            flash("Instructor deleted successfully", "success")
            return redirect('/delete_instructor')
        else:
            flash("There's no instructor with this email id", "error")
            redirect("/delete_instructor")
    return render_template("delete.html", form=form)

@app.route('/delete_student', methods=['POST', 'GET'])
# @admin_permission.require()
@login_required
def delete_student():
    form = DeleteInfo()
    if form.validate_on_submit():
        user = manager.get_info(Student, form.email.data)
        if user:
            manager.delete_info(user)
            flash("Student deleted successfully", "success")
            return redirect('/delete_student')
        else:
            flash("There's no student with this email id", "error")
            redirect("/delete_student")
    return render_template("delete.html", form=form)

@app.route('/logout_admin', methods=['POST', 'GET'])
# @admin_permission.require()
@login_required
def logout_admin():
    logout_user()
    return redirect("/admin")


