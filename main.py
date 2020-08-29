from flask import Flask, render_template, request, session, escape, redirect, flash, url_for
from os import path,walk
# from scripts.get_ip import get_ip
from get_ip import get_ip
from scan import load_services, check_local_services, check_network_machines
from flask_sqlalchemy import sqlalchemy,SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dbmodel import Users, Properties, Services
# from dbmodel import Users

import os

dbdir = "sqlite:///"+ os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = '1232314341rdfamkpsva3k1fksapanwp3np3pma'
# app.config["extend_existing"] = True
db = SQLAlchemy(app)
access = {
    'guest':0,
    'user':1,
    'admin':2,
    'super_admin':3 
}

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

def loged_user():    
    if 'username' in session:
        return escape(session['username'])
    else:
        return 'guest'
    
def get_user_access(username):
    user_access = 0    
    if not username == 'guest':
        user = Users.query.filter_by(name=username).first()
        if user:
            user_access = user.access_code
    return int(user_access)


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
                path_pic =path.join(cp,i)
                if not path.exists(path_pic):
                    path_pic = 'static/img/services/PNCmdr.png'
                    
                services.append((i[:i.find('.')],path_pic))
    # print(services)
    # print(final_list)
    return services

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
    
    # return [[ 'emby', '8096'], ['PNCmdr', '2357']]

@app.route('/debug')
def debug():
    user = loged_user()
    return render_template('server_up.html',title='Debug', content='Server is Up!', paragraph='The Server is Up and running ('+get_ip()+')', user=user ,services=get_services(), header_title='Prime Networks Server')

@app.route('/')
def root():
    user = loged_user()
    
    check_network_machines(db, get_user_access(loged_user()))
    return render_template('home.html', user=user, machines=scan_network(get_user_access(loged_user()))['PNCmdr'], header_title='Prime Networks Commander', services=scan_network(get_user_access(user)).keys())

#TODO return only the info corresponding to the acces of the User
@app.route('/scan/<string:username>')
@app.route('/scan')
def scan_network(username='guest'):
    user_acces = get_user_access(username)
    return check_network_machines(db, user_acces)

@app.route('/services')
def return_active_services():
    return check_local_services(db)

@app.route('/login', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['submit'] == 'Login':
            user = Users.query.filter_by(name=request.form['username']).first()
            if user and not user.name == '' and check_password_hash( user.pwd, request.form['password']):
                session['username'] = user.name
                return redirect('/')
            else:
                flash('Wrong Credentials', 'warning')
                return render_template('login.html')
        else:
            # print(request.form["username"])
            try:
                ciphered_pwd = generate_password_hash(request.form["password"], method='sha256')
                new_user = Users(name=request.form["username"], pwd=ciphered_pwd, access_name='guest', access_code=0)
                db.session.add(new_user)
                db.session.commit()
                flash('User Registered Succesfully', 'success')
            except:
                flash('Registration Failed', 'error')
   
            return render_template('login.html')
    # if request.method == 'GET':
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session: 
        session.pop('username')
    return redirect('/')
    
#TODO Check user access
@app.route('/manage', methods=['GET', 'POST'])
@app.route('/manage/users' , methods=['GET', 'POST'])
def manage_page_users():
    if request.method == 'POST':
        if request.form['submit-user'] == 'Create':
            try:
                ciphered_pwd = generate_password_hash(request.form["password"], method='sha256')
                new_user = Users(name=request.form["name"], pwd=ciphered_pwd, access_name=request.form['access_name'], access_code=access[request.form['access_name']], user_categories = access.keys())
                db.session.add(new_user)
                db.session.commit()
            except:
                pass
                # return render_template('login.html', warning=True)
    return render_template('manage.html', header_title='Manage Users', login='True', user='test', property='users', data=get_data('users'),  user_categories = access.keys())

@app.route('/manage/services', methods=['GET', 'POST'])
def manage_page_services():
    if request.method == 'POST':
        if request.form['submit-service'] == 'Create':
            try:
                # ciphered_pwd = generate_password_hash(request.form["password"], method='sha256')
                new_service = Services(name=request.form["name"], port=request.form['port'], access_name=request.form['access_name'], access_code=access[request.form['access_name']], user_categories = access.keys())
                db.session.add(new_service)
                db.session.commit()
            except:
                pass
       
    return render_template('manage.html', header_title='Manage Services', login='True', user='test', property='services', data=get_data('services'),  user_categories = access.keys())

def init_db():
    users = get_data('users')
    if users == None or len(users) == 0:
        ciphered_pwd = generate_password_hash('toor', method='sha256')
        new_user = Users(name='god', pwd=ciphered_pwd, access_name='super_admin', access_code=access['super_admin'])
        db.session.add(new_user)
        db.session.commit()

    services = get_data('services')
    if services == None or len(services) == 0:
        new_service = Services(name='PNCmdr', port='2357', access_name='admin', access_code=access['guest'])
        db.session.add(new_service)
        db.session.commit()

if __name__ == '__main__':
    db.create_all()
    init_db()
    os.popen("sass static/scss/style.scss:static/css/style.css")
    session = {}
    app.run(debug=True,host=get_ip(), port=2357)