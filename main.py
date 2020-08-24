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
# app.config["extend_existing"] = True
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    pwd = db.Column(db.String(80), nullable=False)
    access_guest = db.Column(db.Boolean)
    access_user = db.Column(db.Boolean)
    access_admin = db.Column(db.Boolean)
    access_superadmin = db.Column(db.Boolean)

class services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    port = db.Column(db.String(5), unique=True, nullable=False)
        

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Users.query.filter_by(name=request.form['username']).first()
        print(user.name)
        if user and check_password_hash( user.pwd, request.form['password']):
            return str("Wellcome "+str(user.name))
        else:
            return "Try Angain"
    return render_template('login.html', action='/login')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        ciphered_pwd = generate_password_hash(request.form["password"], method='sha256')
        new_user = Users(name=request.form["username"], pwd=ciphered_pwd, access_guest=True, access_user=False, access_admin=False, access_superadmin=False)
        db.session.add(new_user)
        db.session.commit()
        return 'user Registered'
    # if request.method == 'GET':
    return render_template('login.html', action='/register')


#TODO Check user access
@app.route('/manage')
def manage_page():
    return render_template('manage.html', header_title='Manage', login='True', user='test')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=2357)