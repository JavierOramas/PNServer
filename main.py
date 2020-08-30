
import os

from get_ip import get_ip
from scan import load_services, check_local_services, check_network_machines
from dbmodel import Users, Properties, Services, app, db

from components.base.content_endpoints import debug, root, logout, login, scan_network, manage_page_users, manage_page_services, loged_user, get_user_access, get_services, get_data, init_db

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
@app.route('/manage', methods=['GET', 'POST'])
@app.route('/manage/users' , methods=['GET', 'POST'])
def route_manage_users():
    return manage_page_users()

@app.route('/manage/services', methods=['GET', 'POST'])
def route_manage_sevices():
    return manage_page_services()


if __name__ == '__main__':

    db.create_all()
    init_db()
    os.popen("sass static/scss/style.scss:static/css/style.css")
    session = {}
    app.run(debug=True,host=get_ip(), port=2357)