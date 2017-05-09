from flask import Flask, render_template, redirect
import RPi.GPIO as GPIO
import subprocess
import os
import datetime
import time
app = Flask(__name__)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

outPin = [6, 13, 19, 26]


GPIO.setup(outPin, GPIO.OUT, initial=GPIO.HIGH)

@app.route("/")
def hello():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %I:%M %p")
	pin1s= not GPIO.input(outPin[0])
	pin2s= not GPIO.input(outPin[1])
	pin3s= not GPIO.input(outPin[2])
	pin4s= not GPIO.input(outPin[3])
	if pin1s is False:
		pin1I= "/static/Fan.png"
	else:
		pin1I= "/static/Fan1.png"
	if pin2s is False:
		pin2I= "/static/FL.png"
	else:
		pin2I= "/static/FL1.png"
	if pin3s is False:
		pin3I= "/static/BL.png"
	else:
		pin3I= "/static/BL1.png"
	if pin4s is False:
		pin4I= "/static/L.png"
	else:
		pin4I= "/static/L1.png"
	templateData = {
		'title' : 'WebGPIO',
		'time': timeString,
		'url1': pin1I,
		'url2': pin2I,
		'url3': pin3I,
		'url4': pin4I
	}
	return render_template('main.html', **templateData)

@app.route("/pin/<switchNumber>/")
def toggle(switchNumber):
	print(switchNumber)
	state= not GPIO.input(outPin[switchNumber])
	GPIO.output(outPin[switchNumber],state)
	#subprocess.call(['./echo.sh'], shell=True)
	return redirect("/", code=302)



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8000, debug=True)
