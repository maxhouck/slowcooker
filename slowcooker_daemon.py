import json
import fcntl
import os
import RPi.GPIO as GPIO
import time
import MAX31855

from enum import Enum

hysteresis = 3
LOCK_PATH = "/home/pi/slowcooker/lockfile"
lockfile = open(LOCK_PATH, "w+")

def check_alarm():
    alarmtime = status_dict["alarm"]
    currenttime = time.time()
    print("current time is ",currenttime)
    print("alarm time is ",alarmtime)
    if currenttime >= alarmtime :
        return True
    else:
        return False

def update_coil():
    global status_dict
    coil1_pin = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(coil1_pin, GPIO.OUT)
    status_dict["coil_status"] = GPIO.input(coil1_pin)
    if status_dict["coil_activate"] != status_dict["coil_status"] : #if they dont match, change pins and reset coil_status
        print("coil_status changed to", status_dict["coil_activate"])
        GPIO.output(coil1_pin, status_dict["coil_activate"])
        status_dict["coil_status"] = GPIO.input(coil1_pin)

def get_temperature(): #needs to be implemented
    csPin =22
    misoPin = 9
    mosiPin = 10
    clkPin = 11
    max = MAX31855.max31855(csPin,misoPin,mosiPin,clkPin)
    temp = max.readTemp()
    GPIO.cleanup()
    print(temp)
    return temp
    return 100


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

#load json file
json_file =  open('slowcooker_status.json', 'r')
status_dict = json.load(json_file)
json_file.close()
status_dict["temperature_actual"] = get_temperature()

if status_dict["device_status"] == "off":
    print("status is off")

elif status_dict["device_status"] == "waiting":
    print("status is waiting")
    alarm = check_alarm()
    if alarm: #transition to heating state
        status_dict["device_status"] = "HEATING"
        status_dict["coil_activate"] = True
        status_dict["alarm"] = time.time() + int(status_dict["cooktime"])*60

elif status_dict["device_status"] == "HEATING":
    print("status is HEATING")
    alarm = check_alarm()
    if alarm: #transition to Off
        status_dict["device_status"] = "off"
        status_dict["coil_activate"] = False
    elif status_dict["temperature_actual"] > (hysteresis + status_dict["temperature_target"]):
        status_dict["device_status"] = "COOLING"
        status_dict["coil_activate"] = False

elif status_dict["device_status"] == "COOLING":
    print("status is COOLING")
    alarm = check_alarm()
    if alarm: #transition to Off
        status_dict["device_status"] = "off"
        status_dict["coil_activate"] = False
    elif status_dict["temperature_actual"] < (status_dict["temperature_target"] - hysteresis):
            status_dict["device_status"] = "HEATING"
            status_dict["coil_activate"] = True

elif status_dict["device_status"] == "debug":
    print("status is debug")

update_coil()
#write json
json_file =  open('slowcooker_status.json', 'w')
json.dump(status_dict, json_file, indent=4, sort_keys=True)
fcntl.lockf(lockfile, fcntl.LOCK_UN) #release lockfile

lockfile.close()
json_file.close()
