from flask_sqlalchemy import sqlalchemy,SQLAlchemy
from flask import Flask

app = Flask('__main__')
db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    pwd = db.Column(db.String(80), nullable=False)
    access_code = db.Column(db.String(5), nullable=False)
    access_name = db.Column(db.String(10), nullable=False)
    
class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    port = db.Column(db.String(5), unique=True, nullable=False)
    access_code = db.Column(db.String(5), nullable=False)
    access_name = db.Column(db.String(10), nullable=False)
       
class Properties(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    access_code = db.Column(db.String(5), nullable=False)
    access_name = db.Column(db.String(10), nullable=False)
