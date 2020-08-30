from flask import Flask
import pandas as pd
from os import path, popen, system
from components.temp_monitor.utils import list_disks
import psutil
from main import app
from os import path,walk
from main import app


#TODO make a god home Page
def temp_api():
    return 'temp_monitor_api'

def get_temps():
    system('python3 '+ path.join(path.dirname(path.abspath(__file__)),'script.py'))
    json_file = pd.read_json(path.join(path.dirname(path.abspath(__file__)),'data/temp.json'), lines=True, convert_dates=False, dtype=float).to_dict(orient='dict')
    json_file['n_cores'] = len(psutil.sensors_temperatures()['coretemp'])-2
    json_file['disks_name'] = list_disks()
    return json_file
    # return pd.read_json(path.join(path.dirname(path.abspath(__file__)),'data/temp.json'), lines=True, convert_dates=False, dtype=float).to_dict(orient='dict')
def get_history():
    json_file = pd.read_json(path.join(path.dirname(path.abspath(__file__)),'data/history.json'), lines=True, convert_dates=False, dtype=float).to_dict(orient='dict')
    json_file['n_cores'] = len(psutil.sensors_temperatures()['coretemp'])-2
    json_file['disks_name'] = list_disks()
    return json_file

def measure():
    system('python3 '+ path.join(path.dirname(path.abspath(__file__)),'script.py get_temperatures'))
    system('python3 '+ path.join(path.dirname(path.abspath(__file__)),'script.py get_cpu_load'))
    return "OK"

def clean():
    system('python3 '+ path.join(path.dirname(path.abspath(__file__)),'clean.py')+' 100')
    return "OK"