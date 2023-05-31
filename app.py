from flask import Flask, render_template, jsonify, flash, request, redirect, url_for
from sqlalchemy import create_engine, text
#from flask_login import UserMixin
#from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from database import get_users_from_db, load_user_from_db, add_user_to_db


from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from file_up_down import upload_file_to_dropbox, downlad_file_from_dropbox


app = Flask(__name__)
csrf = CSRFProtect(app)

#for DataBase
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route("/")
def home():
  users = get_users_from_db()
  return render_template('home.html', users=users, company_name='NeoClarity')


@app.route("/dashboard")
def dashboard():
  data = [
    ("01-01-2020", 1597),
    ("02-01-2020", 1456),
    ("03-01-2020", 1908),
    ("04-01-2020", 895),
    ("05-01-2020", 755)
  ]
  labels = [row[0] for row in data]
  values = [row[1] for row in data]
  return render_template('dashboard.html', values=values, labels=labels)


class UpLoad_Form(FlaskForm):
  journal = FileField("Joural.txt")
  submit = SubmitField("Upload")

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
  print("on upload_file")
  with open(os.path.join('static', 'test.txt'), 'rb') as f:
    upload_file_to_dropbox(f, '/aicoach/test.txt')
    return 'File Uploaded'
  return 'No file uploaded'


@app.route('/download_file', methods=['GET', 'POST'])
def download_file():
  print("in download_file")
  #TODO: get file_url from DataBase
  content = downlad_file_from_dropbox('/aicoach/test.txt')
  return render_template('download_file.html', content=content)

class SignUpForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  fname = StringField("First name", validators=[DataRequired()])
  sname = StringField("Sure name", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired()])
  password_hash = PasswordField("Password", validators=[DataRequired(),
                  EqualTo('password_hash2', message='Passwords Must Match!')])
  password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
  journal = FileField("Journal txt")
  submit = SubmitField("Submit")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("at signup")
    username = None
    form = SignUpForm()
    print("form data: ", request.form)  # print form data
    print("nodata", form.username)
    print("data", form.username.data)
    if form.validate_on_submit():
        print("form is valid")
        username = load_user_from_db(form.username.data)
        if username is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = {
                'username': form.username.data,
                'fname': form.fname.data,
                'sname': form.sname.data,
                'email': form.email.data,
                'password_hash': hashed_pw,
                'journal': form.journal.data
            }
            add_user_to_db(user)
            flash("User Added Successfully!")
        our_users = get_users_from_db()
        return render_template("users.html", form=form, username=username, our_users=our_users)
    else:
        print("form is invalid, errors: ", form.errors)  # print form errors
        return render_template("signup.html", form=form)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("at login")
    form = LoginForm()
    if form.validate_on_submit():
        print("Username from Form: " + form.username)
        user = load_user_from_db(form.username)
        print(user)
        if user:
            # Check Hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfull!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Does Not Exist")
    return render_template("login.html", form=form)

@app.route('/users')
def users():
  users = get_users_from_db()
  return render_template("users.html", users=users)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
