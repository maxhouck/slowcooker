import json
import RPi.GPIO as GPIO
import time
from enum import Enum

#enum off, idle, heating, cooling
class device_status(Enum):
    OFF = 1
    WAITING = 2
    HEATING = 3
    COOLING = 4

coil1_pin = 24
coil2_pin = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(coil1_pin, GPIO.OUT)
GPIO.output(coil1_pin, GPIO.LOW)
GPIO.setup(coil2_pin, GPIO.OUT)
GPIO.output(coil2_pin, GPIO.LOW)

#load json file
with open('slowcooker_status.json', 'r+') as json_file:
    status_dict = json.load(json_file)
    for key in status_dict:
        print key

#check alarm
currenttime = time.localtime(time.time())
if currenttime >= status_dict["alarm"]["time"] :
    print("alarm sounded ring ring ring")
    status_dict["coil_activate"] = True
    if status_dict["device_status"] == 2:
        status_dict["device_status"] = 3
    #set a new alarm for when to turn off
else:
    print("no alarm yet")

#update pins
status_dict["coil_status"] = GPIO.input(coil2_pin)
if status_dict["coil_activate"] != status_dict["coil_status"] : #if they dont match, change pins and reset coil_status
    print("coil_status changed to", status_dict["coil_activate"])
    GPIO.output(coil1_pin, status_dict["coil_activate"])
    GPIO.output(coil2_pin, status_dict["coil_activate"])
    status_dict["coil_status"] = GPIO.input(coil2_pin)


#write json
json.dump(status_dict, json_file)

close(json_file)
GPIO.cleanup()


def check_alarm(alarmtime):
    currenttime = time.localtime(time.time())
    if currenttime >= alarmtime :
        print("alarm sounded ring ring ring")
        status = Status.heating;
    else:
        print("no alarm yet")

def update_outputs():
    if coil1_status != GPIO.input(coil1_pin) :
        print("coil1_status changed to", coil1_status)
    if coil2_status != GPIO.input(coil2_pin) :
        print("coil2_status changed to", coil2_status)
    GPIO.output(coil1_pin, coil1_status)
    GPIO.output(coil2_pin, coil2_status)
