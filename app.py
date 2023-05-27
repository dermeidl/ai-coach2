from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, text
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from database import get_users_from_db


app = Flask(__name__)


@app.route("/")
def home():
  users = get_users_from_db()
  return render_template('home.html', users=users, company_name='NeoClarity')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

