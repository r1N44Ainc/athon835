from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import random

# Flask App connection
app = Flask(__name__)
# SQLite connect
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shedule.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

conn = sqlite3.connect("shedule.db")


class Corpus(db.Model):
    __tablename__ = 'corpus'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('NAME', db.String(200), nullable=False)


class Auditory(db.Model):
    __tablename__ = 'auditory'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('USER', db.String(200), nullable=False)
    id_corpus = db.Column('ID_CORPUS', db.String, db.ForeignKey(Corpus.id), nullable=False)


class Day(db.Model):
    __tablename__ = 'day'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('NAME', db.String(50), nullable=False)
    short = db.Column('SHORT', db.String(50), nullable=False)


class Faculty(db.Model):
    __tablename__ = 'faculty'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('NAME', db.String(200), nullable=False)


class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('NAME', db.String(200), nullable=True)


class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('NAME', db.String(200), primary_key=True, nullable=False)


class Structure(db.Model):
    __tablename__ = 'structure'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('NAME', db.String(200), nullable=False)


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('NAME', db.String(50), nullable=False)
    course = db.Column('COURSE', db.String(200), nullable=True)
    id_faculty = db.Column('ID_FACULTY', db.String, db.ForeignKey(Faculty.id), nullable=False)
    id_structure = db.Column('ID_STRUCTURE', db.String, db.ForeignKey(Structure.id), nullable=False)
    id_level = db.Column('ID_LEVEL', db.String, db.ForeignKey(Level.id), nullable=False)


class User(db.Model):
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('NAME', db.String(200), nullable=False)
    login = db.Column('LOGIN', db.String(200), nullable=False)
    password = db.Column('PASSWORD', db.String(200), nullable=False)
    token = db.Column('TOKEN', db.String(38), nullable=False)
    expiration = db.Column('EXPIRATION', db.DateTime, nullable=False)


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    id_user = db.Column('ID_USER', db.String, db.ForeignKey(User.id), nullable=True)
    method = db.Column('METHOD', db.String(6), nullable=False)
    url = db.Column('URL', db.String(500), nullable=False)
    status = db.Column('STATUS', db.String, nullable=False)
    ip = db.Column('IP', db.String, nullable=False)
    time = db.Column('TIME', db.DateTime, nullable=False)


class Time(db.Model):
    __tablename__ = 'time'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    beg = db.Column('BEG', db.DateTime, nullable=False)
    end = db.Column('END', db.DateTime, nullable=False)


class Shedule(db.Model):
    __tablename__ = 'shedule'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    id_lesson = db.Column('ID_LESSON', db.String, db.ForeignKey(Lesson.id), nullable=False)
    id_day = db.Column('ID_DAY', db.String, db.ForeignKey(Day.id), nullable=False)
    id_group = db.Column('ID_GROUP', db.String, db.ForeignKey(Group.id), nullable=False)
    id_auditory = db.Column('ID_AUDITORY', db.String, db.ForeignKey(Auditory.id), nullable=False)
    id_time = db.Column('ID_TIME', db.String, db.ForeignKey(Time.id), nullable=False)
    week = db.Column('WEEK', db.String(1000), nullable=False)


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column('ID', db.String, primary_key=True, nullable=False)
    name = db.Column('NAME', db.String(200), nullable=False)


class TeacherShedule(db.Model):
    __tablename__ = 'teacher_shedule'
    id_teacher = db.Column('ID_TEACHER', db.String, db.ForeignKey(Teacher.id), primary_key=True, nullable=False)
    id_shedule = db.Column('ID_SHEDULE', db.String(200), db.ForeignKey(Shedule.id), nullable=False)


def UserChanges(nid, nname, nlogin, npassword, ntoken, nexpiration):
    user = User(id=nid, name=nname, login=nlogin, password=npassword, token=ntoken, expiration=nexpiration)
    try:
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    except:
        return print("При добавлении произошла ошибка")
    else:
        return print("Else - return")