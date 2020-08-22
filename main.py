from flask import Flask, render_template
from os import path,walk
from scripts.get_ip import get_ip

app = Flask(__name__)

@app.route('/debug')
def get_services():
    services = []
    for cp,dir,files in walk('static/img/services'):
        for i in files:
            services.append((i[:i.find('.')],path.join(cp,i)))
    return services
def debug():
    return render_template('server_up.html',title='Debug', content='Server is Up!', paragraph='The Server is Up and running ('+get_ip()+'), if you expected someting diferent than this erase cache in your web browser', services=get_services())

@app.route('/')
def root():
    return debug()

#TODO Database to store users for the Machine
#TODO Register new users in the database

if __name__ == '__main__':
    app.run(debug=True,port=2357)