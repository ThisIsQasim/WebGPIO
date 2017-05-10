from flask import Flask, render_template, redirect, Markup
import RPi.GPIO as GPIO
import subprocess
import os
import datetime
import time
app = Flask(__name__)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

outPin = [6, 13, 19, 26]
pinName= ['Fan', 'Front Light', 'Back Light', 'Bright Light']

GPIO.setup(outPin, GPIO.OUT, initial=GPIO.HIGH)

@app.route("/")
def main():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %I:%M %p")
	pinState = []
	for i in range(len(outPin)):
		if GPIO.input(outPin[i]) is 1:
			pinState.append('containerOff')
		else:
			pinState.append('containerOn')
	passer = ''
	for j in range(len(outPin)):
		pinHtmlName = pinName[j].replace(" ", "<br>")
		passer = passer + "<button class='%s' formaction='/pin/%d/'>%s</button>" % (pinState[j], j, pinHtmlName)

	buttonList = Markup(passer)
	templateData = {
		'title' : 'WebGPIO',
		'time': timeString,
		'buttons' : buttonList
	}
	return render_template('main.html', **templateData)

@app.route("/pin/<int:switchNumber>/")
def toggle(switchNumber):
	#print(switchNumber)
	state= not GPIO.input(outPin[switchNumber])
	GPIO.output(outPin[switchNumber],state)
	#subprocess.call(['./echo.sh'], shell=True)
	return redirect("/", code=302)



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8000, debug=True)
