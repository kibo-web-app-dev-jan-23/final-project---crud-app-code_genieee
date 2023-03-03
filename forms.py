from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField
from wtforms.validators import InputRequired, Length, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = "Don'tTellAnyone"


class Signup(FlaskForm):
    firstName = StringField("Firstname", validators=[InputRequired()])
    lastName = StringField("Lastname", validators= [InputRequired()])
    username= StringField("Username", validators=[InputRequired()])
    email = EmailField("Email-Id", validators=[InputRequired(), Email(message="Input a valid email address")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])
    dateOfBirth = DateField("Date-of-birth", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    
class Login(FlaskForm):
    username = StringField("Username/email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])
    
@app.route('/', methods=["GET", "POST"])
def signup():
    form = Signup()
    if form.validate_on_submit():
        return "Form Successfully Submitted!"
    return render_template("signup.html", form= form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        return "Form Successfully Submitted!"
    return render_template("login.html", form= form)