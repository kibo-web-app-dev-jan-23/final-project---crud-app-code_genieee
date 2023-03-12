# Importing necessary modules
from flask import Flask, render_template, redirect, url_for, flash, current_app
from db_manager import SchoolManagementDB, generate_random_password
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from forms import Add_student, AddInstructor, Login, AdminLogin, ChangePasswordForm, ViewClass, SearchInfo, DeleteInfo, get_data_from_form, get_data_from_login_form
from models import Student, Instructors
from pyisemail import is_email





# Initializing the Flask app and setting the secret key
app = Flask(__name__)
app.config['SECRET_KEY'] = "Don'tTellAnyone"
app.config['USE_SESSION_FOR_NEXT'] = True
# Initializing the Bcrypt module to hash the passwords
bcrypt = Bcrypt(app)


# Initializing the LoginManager to handle user authentication
login_manager = LoginManager()
login_manager.init_app(app)
# Initializing the SchoolManagementDB class to interact with the database
manager = SchoolManagementDB()
manager.initialize_db_schema()



# Defining the user loader function for the LoginManager
# This function is called to get the user object based on the user id
@login_manager.user_loader
def load_user(id):
    user= manager.query_db(id)
    return (user)



# Routing
# Defining the routes for the application
# Homepage route
@app.get("/")
@app.get("/home")
def homepage():
    return render_template("home.html")

# Student login route   
@app.route('/student_login', methods=["GET", "POST"])
def student_login():
    # Creating an instance of the Login form
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


# Instructor login route
@app.route('/instructor_login', methods=["GET", "POST"])
def instructor_login():
    # Creating an instance of the Login form
    form = Login()
    if form.validate_on_submit():
        # Getting the username and password from the login form
        username, password = get_data_from_login_form(form)
        # Checking if the user exists in the database
        user = manager.get_info(Instructors, username)
        if user:
            # Checking if the password matches the hashed password in the database
            if bcrypt.check_password_hash(user.password, password):
                # Logging in the user and redirecting to the homepage
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


# Route for changing a student's password
@app.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
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

# Set up route for admin login page
@app.route('/admin', methods=["GET", "POST"])
def admin_login():
    # Create instance of AdminLogin form
    form = AdminLogin()
    # Generate hashed password from user's input password
    password = bcrypt.generate_password_hash(form.password.default).decode('utf-8')

    # If admin does not exist, initialize data
    if manager.get_admin_info(form.username.default)==None:
        manager.initialize_data(form.username.default, password)
        # If form is submitted and validated, check admin credentials and redirect to homepage if successful
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
        # If admin exists, check admin credentials and redirect to homepage if successful
        if form.validate_on_submit():
            username, password = get_data_from_login_form(form)
            user = manager.get_admin_info(username)
            print(current_user.role_id)
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
    # Render admin login page with AdminLogin form            
    return render_template("admin.html", form= form)

# Set up route for admin homepage
@app.route("/admin_homepage", methods=["GET", "POST"])
@login_required
def admin_homepage():
    # Render admin homepage
    return render_template("admin_homepage.html")

# Set up route for adding an instructor
@app.route("/add_instructor", methods=["GET", "POST"])
@login_required
def add_instructors():
    # Create an instance of the form for adding an instructor
    form = AddInstructor()
    # Generate a random password for the instructor
    password = generate_random_password()
    # Hash the password for security
    secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
    if form.validate_on_submit():
        # Check if the email address is valid
        if is_email(form.email.data, check_dns=True) == False:
            flash("Email does not exist", "error")
            redirect("/add_instructor")
        
        else:
            # Check if the instructor has already been registered
            if manager.get_info(Instructors, form.email.data) == None:
                # Add the instructor to the database
                manager.add_instructor(form.firstName.data, form.lastName.data, form.email.data, secure_password)
                flash(f"Instructor added successfully. Instructor's password is {password}", "success")
                # Redirect to the page for adding an instructor
                return redirect("/add_instructor")
            else:
                flash("This instructor has been registered", "error")
    # Render the template for adding an instructor            
    return render_template("instructor.html", form=form)


# Define a route to add a new student to the database
@app.route('/add_student', methods=["GET", "POST"])
@login_required
def add_student():
    form = Add_student()
    password = generate_random_password()
    secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
    firstname,lastname,email,dob,address,year = get_data_from_form(form)
    if form.validate_on_submit():
        # Validate email using email_validator module
        if is_email(email, check_dns=True) == False:
            flash("Email does not exist", "error")
            redirect("/add_student")
        else:
            check_student = manager.get_info(Student, email)
            if check_student == None:
                # Add student to database
                manager.add_student(firstname,lastname,email,secure_password,dob,address, year)
                flash (f"Student added successfully. Student password is {password}", "success")
                return redirect("/add_student")
            else:
                flash ("The email you entered has been used by a student", "error")
                redirect("/add_student")
    return render_template("add_student.html", form= form)


# Define a route to view students in a class
@app.route("/view_class", methods=["GET", "POST"])
@login_required
def view_class():
    form = ViewClass()
    if form.validate_on_submit():
        # Get student data from database based on the year selected
        if form.select_year.data == "Year 1":
            result = manager.view_student_in_a_class(1)
        elif form.select_year.data == "Year 2":
            result = manager.view_student_in_a_class(2)
        elif form.select_year.data == "Year 3":
            result = manager.view_student_in_a_class(3)
        return render_template("student.html", result=result)    
    return render_template("view_class.html", form = form)

# Route for displaying all instructors
@app.route("/view_instructors", methods=["GET", "POST"])
@login_required
def view_all_instructors():
    # Get all instructors from the manager
    result = manager.get_all_instructors()
    return render_template("available_instructors.html",result=result)


# Route for searching for a student
@app.route('/search_student', methods=['POST', 'GET'])
@login_required
def search_for_student():
    # Create an instance of the SearchInfo form
    form = SearchInfo()
    # If the form is submitted and valid, look up the student and render the student.html template with the result
    if form.validate_on_submit():
        result = manager.lookup(Student, form.first_name.data, form.last_name.data)
        if result:
            return render_template("student.html", result=result)
        else:
            # If the student is not found, flash an error message and redirect to the search_student route
            flash("Student does not exist", "error")
            return redirect("/search_student")
    return render_template("search.html", form=form) 

# Route for searching for an instructor
@app.route('/search_instructor', methods=['POST', 'GET'])
@login_required
def search_for_instructor():
    # Create an instance of the SearchInfo form
    form = SearchInfo()
    # If the form is submitted and valid, look up the instructor and render the available_instructor.html template with the result
    if form.validate_on_submit():
        result = manager.lookup(Instructors, form.first_name.data, form.last_name.data)
        if result:
            return render_template("available_instructor.html", result=result)
        else:
            # If the instructor is not found, flash an error message and redirect to the search_instructor route
            flash("Instructor does not exist", "error")
            return redirect("/search_instructor")
    return render_template("search.html", form=form) 

# Delete Instructor route
@app.route('/delete_instructor', methods=['POST', 'GET'])
@login_required
def delete_instructor():
    # Create an instance of the DeleteInfo form
    form = DeleteInfo()
    # If the form is submitted and valid
    if form.validate_on_submit():
        # Retrieve the instructor with the given email
        user = manager.get_info(Instructors, form.email.data)
        if user:
            # Delete the instructor and display success message
            manager.delete_info(user)
            flash("Instructor deleted successfully", "success")
            # Redirect to the same page to show updated list of instructors
            return redirect('/delete_instructor')
        else:
            # If the instructor is not found, display error message and redirect to the same page
            flash("There's no instructor with this email id", "error")
            redirect("/delete_instructor")
    return render_template("delete.html", form=form)

# Delete Student route
@app.route('/delete_student', methods=['POST', 'GET'])
@login_required
def delete_student():
    # Create an instance of the DeleteInfo form
    form = DeleteInfo()
    if form.validate_on_submit():
        # Retrieve the student with the given email
        user = manager.get_info(Student, form.email.data)
        if user:
            # Delete the student and display success message
            manager.delete_info(user)
            flash("Student deleted successfully", "success")
            # Redirect to the same page to show updated list of students
            return redirect('/delete_student')
        else:
            # If the student is not found, display error message and redirect to the same page
            flash("There's no student with this email id", "error")
            redirect("/delete_student")
    return render_template("delete.html", form=form)

# Logout route
@app.route('/logout_admin', methods=['POST', 'GET'])
@login_required
def logout_admin():
    # Logout the current user and redirect to the admin page
    logout_user()
    return redirect("/admin")


