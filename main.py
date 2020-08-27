from flask import Flask, render_template, request, session, escape, redirect
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
app.secret_key = '1232314341rdfamkpsva3k1fksapanwp3np3pma'
# app.config["extend_existing"] = True
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    pwd = db.Column(db.String(80), nullable=False)
    access_code = db.Column(db.String(5), unique=True, nullable=False)
    access_name = db.Column(db.String(10), unique=True, nullable=False)
    
class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    port = db.Column(db.String(5), unique=True, nullable=False)
    access_code = db.Column(db.String(5), unique=True, nullable=False)
    access_name = db.Column(db.String(10), unique=True, nullable=False)
       
class Properties(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    access_code = db.Column(db.String(5), unique=True, nullable=False)
    access_name = db.Column(db.String(10), unique=True, nullable=False)


def get_services():
    services = []
    services_db = Services.query.all()
    columns = Services.__table__.columns
    final_list = []
    
    for i in services_db:
        final_list.append(i.name)
        
    for cp,dir,files in walk('static/img/services'):
        for i in files:
            if i[:i.find('.')] in final_list:
                services.append((i[:i.find('.')],path.join(cp,i)))
    # print(services)
    # print(final_list)
    return services

#TODO return list with all the values of the table
def get_data(property):
    if property == 'users':
        users = Users.query.all()
        columns = Users.__table__.columns
        final_list = []
        for i in users:
            final_list.append([i.id, i.name])
        return final_list
    if property == 'services':
        services = Services.query.all()
        columns = Services.__table__.columns
        final_list = []
        for i in services:
            final_list.append([i.id, i.name, i.port])
        return final_list
    else:
        pass
    
    return [[ 'emby', '8096'], ['PNCmdr', '2357']]

def check_session():
    print(session)
    if 'username' in session:
        return escape(session['username'])
    else:
        return None
    
@app.route('/debug')
def debug():
    print(session)
    if 'username' in session:
        user = escape(session['username'])
    else:
        user = None
    return render_template('server_up.html',title='Debug', content='Server is Up!', paragraph='The Server is Up and running ('+get_ip()+')', user=user ,services=get_services(), header_title='Prime Networks Server')

@app.route('/')
def root():
    return debug()

#TODO return only the info corresponding to the acces of the User
@app.route('/scan')
def scan_network():
    return check_network_machines(db)

@app.route('/services')
def return_active_services():
    return check_local_services()

@app.route('/login', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        if request.form['submit'] == 'Login':
            user = Users.query.filter_by(name=request.form['username']).first()
            if user and not user.name == '' and check_password_hash( user.pwd, request.form['password']):
                session['username'] = user.name
                # print(session)
                # return str("Wellcome "+str(user.name))
                return redirect('/')
            else:
                return render_template('login.html', warning=True)
        else:
            # print(request.form["username"])
            try:
                ciphered_pwd = generate_password_hash(request.form["password"], method='sha256')
                new_user = Users(name=request.form["username"], pwd=ciphered_pwd, access_name='guest', access_code=0)
                db.session.add(new_user)
                db.session.commit()
                return 'user Registered'
            except:
                return render_template('login.html', warning=True)
    # if request.method == 'GET':
        
    return render_template('login.html', warning=False)

#TODO Check user access
@app.route('/manage')
@app.route('/manage/users')
def manage_page_users():
    return render_template('manage.html', header_title='Manage Users', login='True', user='test', property='users', data=get_data('users'))

@app.route('/manage/services')
def manage_page_services():
    return render_template('manage.html', header_title='Manage Services', login='True', user='test', property='services', data=get_data('services'))

if __name__ == '__main__':
    db.create_all()
    
    os.popen("sass static/scss/style.scss:static/css/style.css")
    app.run(debug=True,host=get_ip(), port=2357)