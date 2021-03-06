
import os

from flask import redirect
from get_ip import get_ip
from scan import load_services, check_local_services, check_network_machines
from dbmodel import Users, Properties, Services, app, db

from components.base.content_endpoints import debug, root, logout, login, scan_network, get_machines_service
from components.base.content_endpoints import manage_page_users, manage_page_services, loged_user
from components.base.content_endpoints import get_user_access, get_services, get_data, init_db, delete_entry
from components.base.content_endpoints import edit_entry, delete_entry
# from components.temp_monitor.api import get_temps, measure, clean, temp_api

@app.route('/debug')
def route_debug():
    return debug()

@app.route('/')
def route_root():
    return root() 

@app.route('/scan/<string:username>')
@app.route('/scan')
def route_scan(username='guest'):
    return  scan_network(username)

@app.route('/services')
def return_active_services():
    return check_local_services(db)

@app.route('/login', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def route_login():
    return login()

@app.route('/logout')
def route_logout():
    return logout() 
    
#TODO Check user access

@app.route('/<string:service>')
def redirect_service(service:str):
    return get_machines_service(service)
    
@app.route('/manage', methods=['GET', 'POST'])
@app.route('/manage/users' , methods=['GET', 'POST'])
def route_manage_users():
    return manage_page_users()

@app.route('/manage/services', methods=['GET', 'POST'])
def route_manage_sevices():
    return manage_page_services()

@app.route('/delete/<string:table>/<int:id>', methods=['GET', 'POST'])
def route_delete_entry(table, id):
    return delete_entry(table, id)

@app.route('/edit/<string:table>/<int:id>', methods=['GET', 'POST'])
def route_edit_entry(table, id):
    return edit_entry(table, id)
#TODO see how to rediect port 9998 to this route
## Temp Monitor 
# @app.route('/temps')
# def route_temps():
#     return get_temps()

# @app.route('/measure')
# def route_measure():
#     return measure()

# @app.route('/clean')
# def route_temps():
#     return temps()

if __name__ == '__main__':

    db.create_all()
    init_db()
    os.popen("sass static/scss/style.scss:static/css/style.css")
    session = {}
    app.run(debug=True,host=get_ip(), port=2357)