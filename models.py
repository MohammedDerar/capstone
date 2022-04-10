import os
# from tkinter.tix import INTEGER
from xmlrpc.client import DateTime
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgresql://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)
# database_name = "capstone"
# database_path = 'postgresql://postgres:123@localhost:5432/{}'.format(database_name)
  

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(db.Integer, primary_key=True)
  title = Column(String, nullable=False)
  release_date = Column(String, nullable=False)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date}


class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(db.Integer, primary_key=True)
  name = Column(String, nullable=False)
  gender = Column(String, nullable=False)
  age = Column(db.Integer, nullable=False)

  def __init__(self, name, gender, age):
    self.name = name
    self.gender = gender
    self.age = age

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'gender': self.gender,
      'age': self.age}

    