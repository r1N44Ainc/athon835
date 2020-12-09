from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
import hashlib
import random
import sqlite3
from base import (db, Auditory, Corpus, Day, Faculty, Group, Lesson, Level, Log, Shedule, Structure, Teacher, Time, User, TeacherShedule)


# Flask App connection
app = Flask(__name__)
# SQLite connect
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shedule.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def auth(ulogin, upassword):
    user_list = User.query.order_by(User.id).all()
    user_password = None
    for el in user_list:
        if ulogin == el.login:
            user_password = el.password
            break
    else:
        print('Login Failed')
    if upassword == user_password:
        print('Login Succsess')
    return


def userReg(login):
    user_list = User.query.order_by(User.id).all()
    for el in user_list:
        if login != el.login:
            return False
    return True


