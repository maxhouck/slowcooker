import RPi.GPIO as GPIO
import time
import datetime
from flask import Flask, render_template, request, redirect
from threading import Thread
import RPi.GPIO as GPIO
import time
from enum import Enum

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   24 : {'name' : 'coil 1', 'state' : GPIO.LOW},
   25 : {'name' : 'coil 2', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")
def root():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

@app.route("/slowcooker")
def slowcooker():
     # read status of two outputs and alarms
     #output_status = get_output_status()
     # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
         # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins' : pins
            }
         # Pass the template data into the template main.html and return it to the user
        return render_template('main.html', **templateData)

@app.route("/cooknow", methods=["POST"])
def cooknow():
    if request.method == 'POST':
        cooktime = request.form['cooktime']
        cooktemperature = request.form['temperature']
        return redirect("/slowcooker")

@app.route("/toggle1", methods=["GET"])
def toggle1():
    if request.method == 'GET':
        toggle_output(coil1_pin)
        return redirect("/slowcooker")

@app.route("/toggle2", methods=["GET"])
def toggle2():
    if request.method == 'GET':
        toggle_output(coil2_pin)
        return redirect("/slowcooker")

@app.route("/setalarm", methods=["POST"])
def setalarm():
    if request.method == 'POST':
        alarmtime = request.form['alarmtime']
        cooktime = request.form['cooktime']
        cooktemperature = request.form['temperature']
        print(alarmtime)
        return redirect("/slowcooker")
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      GPIO.output(changePin, not GPIO.input(changePin))
      message = "Toggled " + deviceName + "."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : pins
   }

   return render_template('main.html', **templateData)

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

def toggle_output(pin):
    GPIO.output(pin, not GPIO.input(pin))

def main_loop():
    alarmtime = (2019, 2, 27, 5, 41, 21, 3, 1, 0)
    check_alarm(alarmtime)
    alarmtime = (2019, 2, 27, 6, 41, 21, 3, 1, 0)
    check_alarm(alarmtime)
    update_outputs()

    GPIO.cleanup()


if __name__ == "__main__":
    coil1_status = 0
    coil2_status = 0
    coil1_pin = 24
    coil2_pin = 25
    alarmset = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(coil1_pin, GPIO.OUT)
    GPIO.output(coil1_pin, GPIO.LOW)
    GPIO.setup(coil2_pin, GPIO.OUT)
    GPIO.output(coil2_pin, GPIO.LOW)

    threads = []
#    main = Thread(target=main_loop, args=[])
#    main.start()
#    threads.append(main)
    app.run(host='0.0.0.0', port=80, debug=True)
    #for process in threads: #wait until main and server both quit
    #    process.join()
