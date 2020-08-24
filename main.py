from flask import Flask, render_template, request
from os import path,walk
# from scripts.get_ip import get_ip
from get_ip import get_ip
from scan import load_services, check_local_services, check_network_machines
from flask_sqlalchemy import sqlalchemy,SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# from dbmodel import Users

import os

dbdir = "sqlite:///"+ os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    pwd = db.Column(db.String(80), nullable=False)
    # email = db.Column(db.String(30))
    

def get_services():
    services = []
    for cp,dir,files in walk('static/img/services'):
        for i in files:
            services.append((i[:i.find('.')],path.join(cp,i)))
    return services

@app.route('/debug')
def debug():
    return render_template('server_up.html',title='Debug', content='Server is Up!', paragraph='The Server is Up and running ('+get_ip()+')', services=get_services(), header_title='Prime Networks Server')

@app.route('/')
def root():
    return debug()

#TODO return only the info corresponding to the acces of the User
@app.route('/scan')
def scan_network():
    return check_network_machines()

@app.route('/services')
def return_active_services():
    return check_local_services()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        print(dict(request.form))
        print(request.form["username"])
        ciphered_pwd = generate_password_hash(request.form["password"], method='sha256')
        new_user = Users(name=request.form["username"], pwd=ciphered_pwd)
        db.session.add(new_user)
        db.session.commit()
        return 'user Registered'
    # if request.method == 'GET':
    return render_template('login.html')
#TODO Database to store users for the Machine
#TODO Register new users in the database

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=2357)