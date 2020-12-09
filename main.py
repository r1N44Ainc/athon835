from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
import hashlib
import random
import sqlite3
from base import (db, Auditory, Corpus, Day, Faculty, Group, Lesson, Level, Log, Shedule, Structure, Teacher, Time, User, TeacherShedule)
from methods import auth, userReg


# Flask App connection
app = Flask(__name__)
# SQLite connect
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shedule.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/user/<string:name>/<int:id>')
def user(name,id):
    return "User Page " + name + " - " + str(id)


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        login = request.form['login']
        password = request.form['password']
        token = hashlib.md5(bytes(random.randint(1, 10000000))).hexdigest()
        expiration = (datetime.now() + timedelta(days=30))
        user_id = int(User.query.order_by(User.id.desc()).first().id) + 1
        newUser = User(id=user_id, name=name, login=login, password=password, token=token,  expiration=expiration)

        if userReg(login):
            try:
                db.session.add(newUser)
                db.session.commit()
                return redirect('/')
            except:
                return print("При добавлении возникла ошибка")
        else:
            print('Not unique login')
    return render_template('register.html')


@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    if request.method == "GET":
        teacher_list = Teacher.query.order_by(Teacher.id).all()
    return render_template('teachers.html', teacher_list=teacher_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        auth(login, password)
    #    print(login)
    #     print(password)
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug="True")

