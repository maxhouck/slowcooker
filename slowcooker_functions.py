import RPi.GPIO as GPIO
import time
from enum import Enum

class Status(Enum):
    off = 1
    alarm_set = 2
    heating = 3
    idle = 4

#timer_cycle = (ontime:100, temperature:150)
#alarm_cycle = (alarmtuple, ontime:100, temperature:150)

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
