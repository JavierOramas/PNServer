from os import popen
import pandas as pd
import datetime
import time
from main import app, dbdir
from dbmodel import db
def list_disks():
    hdds = []
    for i in popen('lsblk -d'):
        temp = []
        i = i.replace('\n', '')
        for item in i.split(' '):
            if not item == '':
                temp.append(item)
        hdds.append(temp)

    list_hdds = []
    for i in hdds:
        if i[5] == 'disk':
            list_hdds.append(i[0])

    return list_hdds

def clean_digits(string):
    output = ''
    for i in string:
        try:
            num = int(i)
            output = output+i
        except:
            continue
    return output

def filter_date(df, start, end): 
    elems = []
    for i in df['date']:
        elems.append(start <= datetime.datetime.strptime(str(i),'%Y-%m-%d 00:00:00').date() <= end)
        df.reset_index()
    return df[elems]  

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
    