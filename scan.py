import json
from os import path
import shutil
import pandas as pd
import requests
from get_ip import get_ip

def load_services():
    # f = open(path.join('static/data/ports.json'))
    f = open('static/data/ports.json')
    for i in f.readlines():
        services = json.loads(i)
    return services

available_services = {}

#TODO Add Plex, Kodi, SMB and FTP Shares
def check_local_services():

    ip = get_ip()
    services = load_services()


    #PNCmdr
    available_services['PNCmdr'] = [str('http://'+ip+':'+services['PNCmdr'])]
    #Emby
    try:
        r = requests.get(str('http://'+ip+':'+services['emby'])).text
        if r.find('emby'):
            available_services['emby'] = [str('http://'+ip+':'+services['emby'])]
    except:
        pass
    
    #Temp Monitor api
    try:
        r = requests.get(str('http://'+ip+':'+services['temp_monitor_api'])).text
        if not r.find('temp_monitor_api') == -1:
            available_services['temp_monitor_api'] = [str('http://'+ip+':'+services['temp_monitor_api'])]
    except:
        pass
    #Temp Monitor webui
    try:
        r = requests.get(str('http://'+ip+':'+services['temp_monitor'])).text
        if r.find('temp_monitor'):
            available_services['temp_monitor'] = [str('http://'+ip+':'+services['temp_monitor'])]
    except:
        pass
    
    with open('available_services.json', 'w') as json_file:
        json.dump(available_services, json_file)   
    
    return available_services

#TODO Test network Scan    
def check_network_machines():
    
    ip = get_ip()
    services = load_services()

    all_services = check_local_services()
    ip = ip.split('.')
    for i in range(1,256):
        if i == int(ip[-1]):
            continue
        try:
            r = requests.get('http://'+ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(i)+':2357/services')
            if r.status_code == 200:
                new_services = json.loads(r.text)
                for i in new_services:
                    if i in all_services:
                        for j in new_services[i]:
                            all_services[i].append(j)
                    else:
                        all_services[i] = []
                        for j in new_services[i]:
                            all_services[i].append(j)
        except:
            continue
    with open('all_available_services.json', 'w') as json_file:
        json.dump(all_services, json_file)    
    return all_services

