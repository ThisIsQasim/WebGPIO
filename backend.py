from datetime import timedelta
from functools import update_wrapper
from flask import Flask, render_template, redirect, Markup, make_response, request, current_app
import RPi.GPIO as GPIO
import subprocess, os, datetime, time
app = Flask(__name__)


roomName = ['Bed Room', 'Server Room']
accName= [['Fan', 'Front Light', 'Back Light', 'Bright Light'], ['Champ']]
outPin = [[6, 13, 19, 26],[]]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in range(len(outPin)):
	GPIO.setup(outPin[i], GPIO.OUT, initial=GPIO.HIGH)

def accState(roomNumber, accNumber):
	if roomNumber == 0:
		if GPIO.input(outPin[roomNumber][accNumber]) is 1:
			return 'containerOff'
		else:
			return 'containerOn'
	elif roomNumber > 0:
		#get the state of other accesories in other rooms
		return 'containerOff'


def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
	if methods is not None:
		methods = ', '.join(sorted(x.upper() for x in methods))
	if headers is not None and not isinstance(headers, list):
		headers = ', '.join(x.upper() for x in headers)
	if not isinstance(origin, list):
		origin = ', '.join(origin)
	if isinstance(max_age, timedelta):
		max_age = max_age.total_seconds()
	
	def get_methods():
		if methods is not None:
			return methods
		
		options_resp = current_app.make_default_options_response()
		return options_resp.headers['allow']
	
	def decorator(f):
		def wrapped_function(*args, **kwargs):
			if automatic_options and request.method == 'OPTIONS':
				resp = current_app.make_default_options_response()
			else:
				resp = make_response(f(*args, **kwargs))
			if not attach_to_all and request.method != 'OPTIONS':
				return resp
			
			h = resp.headers
			h['Access-Control-Allow-Origin'] = origin
			h['Access-Control-Allow-Methods'] = get_methods()
			h['Access-Control-Max-Age'] = str(max_age)
			h['Access-Control-Allow-Credentials'] = 'true'
			h['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept, Authorization"
			if headers is not None:
				h['Access-Control-Allow-Headers'] = headers
			return resp
						
		f.provide_automatic_options = False
		return update_wrapper(wrapped_function, f)
	return decorator

@app.route("/")
def main():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %I:%M %p")

	passer = ''
	for i in range(len(roomName)):
		passer = passer + "<p class='roomtitle'>%s</p>" % (roomName[i])
		for j in range(len(accName[i])):
			buttonHtmlName = accName[i][j].replace(" ", "<br>")
			passer = passer + "<span id='button%d%d'><button class='%s' onclick='toggle(%d,%d)'>%s</button></span>" % (i, j, accState(i,j), i, j, buttonHtmlName)

	buttonGrid = Markup(passer)
	templateData = {
		'title' : 'WebGPIO',
		'time': timeString,
		'buttons' : buttonGrid
	}
	return render_template('main.html', **templateData)

@app.route("/grid/")
@crossdomain(origin='*')
def grid():
	passer = ''
	for i in range(len(roomName)):
		passer = passer + "<p class='roomtitle'>%s</p>" % (roomName[i])
		for j in range(len(accName[i])):
			buttonHtmlName = accName[i][j].replace(" ", "<br>")
			passer = passer + "<span id='button%d%d'><button class='%s' onclick='toggle(%d,%d)'>%s</button></span>" % (i, j, accState(i,j), i, j, buttonHtmlName)

	return passer

@app.route("/button/<int:roomNumber>/<int:accNumber>/")
@crossdomain(origin='*')
def toggle(roomNumber, accNumber):
	if len(outPin[roomNumber]) != 0:
		state= not GPIO.input(outPin[roomNumber][accNumber])
		GPIO.output(outPin[roomNumber][accNumber],state)
		#subprocess.call(['./echo.sh'], shell=True)
	else:
		#action for other rooms
		subprocess.call(['./echo.sh'], shell=True)
	#print(roomNumber, accNumber)
	buttonHtmlName = accName[roomNumber][accNumber].replace(" ", "<br>")
	passer="<button class='%s' onclick='toggle(%d,%d)'>%s</button>" % (accState(roomNumber,accNumber), roomNumber, accNumber, buttonHtmlName)
	return passer


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8000, debug=True)
