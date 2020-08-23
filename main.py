from flask import Flask, render_template
from os import path,walk
# from scripts.get_ip import get_ip
from get_ip import get_ip
from scan import load_services

app = Flask(__name__)

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
    return load_services()

@app.route('/login')
def login():
    return render_template('login.html')


#TODO Database to store users for the Machine
#TODO Register new users in the database

if __name__ == '__main__':
    app.run(debug=True,port=2357)