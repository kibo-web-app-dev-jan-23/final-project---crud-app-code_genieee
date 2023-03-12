# Multi-model CRUD App

Design and build a web application using Flask or Express.

## Requirements

Your application

- must use Flask or Express
- must use a relational database (Postgresql is recommended, if you would like to deploy your application. SQLite3 is also fine!)
- must have multiple, related database models
- must have features to Create, Read, Update, and Delete some of those models from a web interface
- must be designed such that it works properly on different devices (desktop and mobile)

You must also include a README.md file that
- explains what your app does
- explains the tables in your schema
- explains how to set the app up and run it locally

## Optional components

The following are optional, but not required:

- you may use an ORM library
- you may use a CSS framework
- you may use an API
- you may have users and authentication
- you may use  a library to manage authentication and authorization
- you may deploy your application to the web

## Recommendations

The possibilities for your application are wide and varied. Choosing a scope for your project that you can complete within the time is key.

Before you start coding, you should:
- write out a list of pages in your planned application
- write the routes associated with those pages and their actions
- write out the plan for the models in your schema

You are also highly encouraged to build a scoped-down **Minimum Viable Product** (MVP) first, then add more features after you have it working.

## Notes

- If you choose to start from a Flask or Express starter code template (like [flask-starter](https://github.com/ksh7/flask-starter) or [express-postgres-boilerplate](https://github.com/mateo-io/express-postgres-boilerplate)) you **must** mention it in your README file.

## School Management System
This is a Flask web application that helps manage the records of a school. There are three types of users - students, instructors, and administrators.

## Schema
The schema of the database consists of 3 tables:

students: contains information about each student, including first name, last name, email, password, date of birth, address, and year of study.
instructors: contains information about each instructor, including first name, last name, email, and password.
admin: stores admin username and password
Setting Up
Clone the repository to your local machine using git clone.
Change your working directory to the project directory.
Create a virtual environment with python -m venv env.
Activate the virtual environment with source env/bin/activate.
Install the dependencies with pip install -r requirements.txt.
Create a .env file in the root directory and specify the following environment variables:
SECRET_KEY: A secret key used by Flask to encrypt session cookies.
DATABASE_URL: The URL of the database. For example: sqlite:///school.db.
Run the app with python app.py.

## Using the App
## Homepage
The homepage contains some general information about the app.

## Login
Students and instructors can log in by selecting the Student Login or Instructor Login button on the homepage, respectively. The user will be redirected to a login page where they can enter their email and password.

Administrators can log in by including the /admin route to the address. The user will be redirected to an admin login page where they can enter their username and password.

## Admin
To login as an admin, the username = Admin and Password = Admin200
After logging in as an administrator, the user will be redirected to the admin homepage. From here, the user can add instructors, add students, view classes, search for student or instructor information, and delete student or instructor information.

## Add Instructor
To add an instructor, the administrator must provide the instructor's first name, last name, email address. The instructor's password will be generated automatically and displayed on the page after the instructor is added.

## Add Student
To add a student, the administrator must provide the student's first name, last name, email address, date of birth, address, and year of study. The student's password will be generated automatically and displayed on the page after the student is added.

## View Class
The administrator can view all students in a particular year of study by selecting the year from the dropdown menu.

## Search Info
The administrator can search for student or instructor information by entering a keyword into the search box. The search is case-insensitive and searches the first name, last name, and email address of both students and instructors.

## Delete Info
The administrator can delete student or instructor information by entering the email address of the student or instructor they want to delete. If the email address is not found, an error message will be displayed.

## Student and Instructor
After the student or instructor has logged in, they can change their passwords to anypassword of their choice.

## Not yet implemented
For the sake of this project, we only implemented some few features so as to meetup with the deadline. Some of the other features we'd like to include in our app are
1. Students being able to view their grades
2. Instructors being to assign assignments
3. Students being able to view pending assignments, mark assignment as completed and also view completed assignments
4. Instructors being able to assign grades to students
5. Student being able to check tuition payment status 
