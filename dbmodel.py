from flask_sqlalchemy import sqlalchemy,SQLAlchemy
from flask import Flask
import os

app = Flask('__main__')
dbdir = "sqlite:///"+ os.path.abspath(os.getcwd()) + "/database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = '1232314341rdfamkpsva3k1fksapanwp3np3pma'
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
