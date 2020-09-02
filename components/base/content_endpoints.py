
import os
from os import path,walk
from flask import Flask, render_template, request, session, escape, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from get_ip import get_ip
from scan import load_services, check_local_services, check_network_machines
from dbmodel import Users, Properties, Services, db

## Static ##################################################################################################### 
access = {
    'guest':0,
    'user':1,
    'admin':2,
    'super_admin':3 
}

session = {}

## User #######################################################################################################

def logout():
    if 'username' in session: 
        session.pop('username')
    return redirect('/')

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

## Content ####################################################################################################### 
def debug():
    user = loged_user()
    return render_template('server_up.html',title='Debug', content='Server is Up!', paragraph='The Server is Up and running ('+get_ip()+')', user=user ,services=get_services(), header_title='Prime Networks Server')

def root():
    user = loged_user()
    
    check_network_machines(db, get_user_access(loged_user()))
    return render_template('home.html', user=user, machines=scan_network(get_user_access(loged_user()))['PNCmdr'], header_title='Prime Networks Commander', services=scan_network(get_user_access(user)).keys())

## Data #########################################################################################################

def scan_network(username='guest'):
    user_acces = get_user_access(username)
    return check_network_machines(db, user_acces)

## Manage #######################################################################################################

def manage_page_users():
    if request.method == 'POST':
        print('here')
        if request.form['submit-user'] == 'Create':
            ciphered_pwd = generate_password_hash(request.form["password"], method='sha256')
            new_user = Users(name=request.form["name"], pwd=ciphered_pwd, access_name=request.form['access_name'], access_code=access[request.form['access_name']])
            db.session.add(new_user)
            db.session.commit()
            # except:
                # pass
                # return render_template('login.html', warning=True)
    return render_template('manage.html', header_title='Manage Users', login='True', user='test', property='users', data=get_data('users'),  user_categories = access.keys(), selected={'name':'', 'pwd':'', 'port': '', 'access_name': ''})

def manage_page_services():
    if request.method == 'POST':
        if request.form['submit-service'] == 'Create':
            try:
                # ciphered_pwd = generate_password_hash(request.form["password"], method='sha256')
                new_service = Services(name=request.form["name"], port=request.form['port'], access_name=request.form['access_name'], access_code=access[request.form['access_name']])
                db.session.add(new_service)
                db.session.commit()
            except:
                pass
            
           
    return render_template('manage.html', header_title='Manage Services', login='True', user='test', property='services', data=get_data('services'),  user_categories = access.keys(), selected={'name':'', 'pwd':'', 'port': '', 'access_name': ''})

def delete_entry(table, id):
    if table == 'users':
        element = Users.query.get(id)
    if table == 'services':
        element = Services.query.get(id)
    db.session.delete(element)
    db.session.commit()
    return redirect('/manage')

def edit_entry(table, id):
    
    if request.method == 'POST':
        if table == 'users':
            
            # try:
            item_id = request.form['id']
            usr = Users.query.filter_by(id=item_id).first()
            if request.form['password'][:5] == 'sha256':
                ciphered_pwd = generate_password_hash(request.form["password"], method='sha256')
                usr.pwd = ciphered_pwd
            usr.name = request.form['name']
            usr.access_name = request.form['access_name']
            usr.access_code = access[request.form['access_name']]
            # db.session.add(usr)
            db.session.commit()
    
        if request.form['save-service'] == 'Save':
            # try:
            ciphered_pwd = generate_password_hash(request.form["password"], method='sha256')
            new_service = Services(name=request.form["name"], port=request.form['port'], access_name=request.form['access_name'], access_code=access[request.form['access_name']])
            db.session.add(new_service)
            db.session.commit()
            # except:
                # pass
    if table == 'users':
        element = Users.query.get(id)
    if table == 'services':
        element = Services.query.get(id)
    return render_template('manage.html', property=table, header_title='Manage '+table, login='True', user='test', data=get_data(table),  user_categories = access.keys(), selected=element)

## Tools #######################################################################################################

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
    