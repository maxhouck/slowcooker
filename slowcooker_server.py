import time
import datetime
from flask import Flask, render_template, request, redirect
import json
import fcntl
import os
from enum import Enum

app = Flask(__name__)

@app.route("/")
def root():
    os.system("python slowcooker_daemon.py")
    LOCK_PATH = "/home/pi/slowcooker/lockfile"
    lockfile = open(LOCK_PATH, "w+")
    while True:
       try:
           fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
           break
       except IOError as e:
           # raise on unrelated IOErrors
           if e.errno != errno.EAGAIN:
               raise
           else:
               time.sleep(0.1)
    json_file = open('slowcooker_status.json', 'r')
    status_dict = json.load(json_file)
    json_file.close()
    fcntl.lockf(lockfile, fcntl.LOCK_UN) #release lockfile
    lockfile.close()
    return render_template('main.html', status_dict = status_dict, time = time.time())

@app.route("/cooknow", methods=["POST"])
def cooknow():
    if request.method == 'POST':
        LOCK_PATH = "/home/pi/slowcooker/lockfile"
        lockfile = open(LOCK_PATH, "w+")
        while True:
            try:
                fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except IOError as e:
                # raise on unrelated IOErrors
                if e.errno != errno.EAGAIN:
                    raise
                else:
                    time.sleep(0.1)
        json_file =  open('slowcooker_status.json', 'r')
        status_dict = json.load(json_file)
        json_file.close()
        json_file =  open('slowcooker_status.json', 'w')
        print(status_dict["alarm"]["set"])
        status_dict["device_status"]="heating"
        status_dict["alarm"]["set"]=True
        status_dict["coil_activate"]=True
        status_dict["alarm"]["time"]=time.time() + int(request.form['cooktime'])*60
        status_dict["temperature_target"]=request.form['temperature']
        json.dump(status_dict, json_file, indent=4, sort_keys=True)
        fcntl.lockf(lockfile, fcntl.LOCK_UN) #release lockfile
        lockfile.close()
        json_file.close()
        return redirect("/")

@app.route("/turnoff")
def turnoff():
    LOCK_PATH = "/home/pi/slowcooker/lockfile"
    lockfile = open(LOCK_PATH, "w+")
    while True:
        try:
            fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except IOError as e:
            # raise on unrelated IOErrors
            if e.errno != errno.EAGAIN:
                raise
            else:
                time.sleep(0.1)
    json_file =  open('slowcooker_status.json', 'r')
    status_dict = json.load(json_file)
    json_file.close()
    json_file =  open('slowcooker_status.json', 'w')
    print(status_dict["alarm"]["set"])
    status_dict["device_status"]="off"
    status_dict["alarm"]["set"]=False
    status_dict["coil_activate"]=False
    status_dict["alarm"]["time"]=0
    status_dict["temperature_target"]=0
    json.dump(status_dict, json_file, indent=4, sort_keys=True)
    fcntl.lockf(lockfile, fcntl.LOCK_UN) #release lockfile
    lockfile.close()
    json_file.close()
    return redirect("/")

@app.route("/cancel")
def cancel():
    LOCK_PATH = "/home/pi/slowcooker/lockfile"
    lockfile = open(LOCK_PATH, "w+")
    while True:
        try:
            fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except IOError as e:
            # raise on unrelated IOErrors
            if e.errno != errno.EAGAIN:
                raise
            else:
                time.sleep(0.1)
    json_file =  open('slowcooker_status.json', 'r')
    status_dict = json.load(json_file)
    json_file.close()
    json_file =  open('slowcooker_status.json', 'w')
    print(status_dict["alarm"]["set"])
    status_dict["device_status"]="off"
    status_dict["alarm"]["set"]=False
    status_dict["coil_activate"]=False
    status_dict["alarm"]["time"]=0
    status_dict["temperature_target"]=0
    json.dump(status_dict, json_file, indent=4, sort_keys=True)
    fcntl.lockf(lockfile, fcntl.LOCK_UN) #release lockfile
    lockfile.close()
    json_file.close()
    return redirect("/")

@app.route("/toggle", methods=["GET"])
def toggle():
    LOCK_PATH = "/home/pi/slowcooker/lockfile"
    lockfile = open(LOCK_PATH, "w+")
    while True:
        try:
            fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except IOError as e:
            # raise on unrelated IOErrors
            if e.errno != errno.EAGAIN:
                raise
            else:
                time.sleep(0.1)
    json_file =  open('slowcooker_status.json', 'r')
    status_dict = json.load(json_file)
    json_file.close()
    json_file =  open('slowcooker_status.json', 'w')
    status_dict["device_status"]="debug"
    status_dict["alarm"]["set"]=False
    status_dict["coil_activate"]=not status_dict["coil_activate"]
    json.dump(status_dict, json_file, indent=4, sort_keys=True)
    fcntl.lockf(lockfile, fcntl.LOCK_UN) #release lockfile
    lockfile.close()
    json_file.close()
    return redirect("/")

@app.route("/setalarm", methods=["POST"])
def setalarm():
    if request.method == 'POST':
        print(request.form['alarmtime'])
        LOCK_PATH = "/home/pi/slowcooker/lockfile"
        lockfile = open(LOCK_PATH, "w+")
        while True:
            try:
                fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except IOError as e:
                # raise on unrelated IOErrors
                if e.errno != errno.EAGAIN:
                    raise
                else:
                    time.sleep(0.1)
        json_file =  open('slowcooker_status.json', 'r')
        status_dict = json.load(json_file)
        json_file.close()
        json_file =  open('slowcooker_status.json', 'w')
        print(status_dict["alarm"]["set"])
        status_dict["device_status"]="waiting"
        status_dict["alarm"]["set"]=True
        split = request.form['alarmtime'].split(':')
        hours = int(split[0])
        minutes = int(split[1])
        alarmtime = time.time() + hours*3600 + minutes*60
        status_dict["alarm"]["time"]=alarmtime
        status_dict["cooktime"]=request.form['cooktime']
        status_dict["temperature_target"]=request.form['temperature']
        print(status_dict["alarm"]["set"])
        json.dump(status_dict, json_file, indent=4, sort_keys=True)
        fcntl.lockf(lockfile, fcntl.LOCK_UN) #release lockfile
        lockfile.close()
        json_file.close()
    return redirect("/")

app.run(host='0.0.0.0', port=80, debug=True)
