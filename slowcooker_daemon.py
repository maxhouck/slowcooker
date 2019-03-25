import json
import fcntl
import os
import RPi.GPIO as GPIO
import time

from enum import Enum

LOCK_PATH = "/home/pi/slowcooker/lockfile"
lockfile = open(LOCK_PATH, "w+")

def check_alarm(alarmtime):
    currenttime = time.localtime(time.time())
    if currenttime >= alarmtime :
        print("alarm sounded ring ring ring")
        status = Status.heating;
    else:
        print("no alarm yet")

def update_coil():
    status_dict["coil_status"] = GPIO.input(coil2_pin)
    if status_dict["coil_activate"] != status_dict["coil_status"] : #if they dont match, change pins and reset coil_status
        print("coil_status changed to", status_dict["coil_activate"])
        GPIO.output(coil1_pin, status_dict["coil_activate"])
        GPIO.output(coil2_pin, status_dict["coil_activate"])
        status_dict["coil_status"] = GPIO.input(coil2_pin)

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

coil1_pin = 24
coil2_pin = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(coil1_pin, GPIO.OUT)
GPIO.output(coil1_pin, GPIO.LOW)
GPIO.setup(coil2_pin, GPIO.OUT)
GPIO.output(coil2_pin, GPIO.LOW)

#load json file
json_file =  open('slowcooker_status.json', 'r')
status_dict = json.load(json_file)
json_file.close()
json_file =  open('slowcooker_status.json', 'w')
for key in status_dict:
    print key

if status_dict["device_status"] == "off":
    print("status is off")
    update_coil()

elif status_dict["device_status"] == "waiting":
    print("status is waiting")
    #check alarm
    currenttime = time.localtime(time.time())
    if currenttime >= status_dict["alarm"]["time"] :
        print("alarm sounded ring ring ring")
        status_dict["coil_activate"] = True
        status_dict["device_status"] =  "heating"
        #set a new alarm for when to turn off
    else:
        print("no alarm yet")
    update_coil()

elif status_dict["device_status"] == "heating":
    print("status is HEATING")
    #check if alarm + cooktime has passed and set state to 1 if so
    #check temperature and set state to 3 or 4
    update_coil()

elif status_dict["device_status"] == "cooling":
    print("status is COOLING")
    #check if alarm + cooktime has passed and set state to 1 if so
    #check temperature and set state to 3 or 4
    update_coil()

elif status_dict["device_status"] == "debug":
    print("status is debug")
    update_coil()

#write json
json.dump(status_dict, json_file, indent=4, sort_keys=True)
fcntl.lockf(lockfile, fcntl.LOCK_UN) #release lockfile

lockfile.close()
json_file.close()
GPIO.cleanup()
