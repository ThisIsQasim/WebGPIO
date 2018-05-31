from datetime import timedelta
from functools import update_wrapper
from flask import Flask, render_template, redirect, Markup, make_response, request, current_app
import RPi.GPIO as GPIO
import subprocess, os, sys, datetime, time, json, yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

rooms=cfg['rooms']
app = Flask(__name__)
secure= False


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for room in rooms:
	for accesory in room['Accesories']:
		if accesory['Type'] == 'Pin':
			GPIO.setup(accesory['Value'], GPIO.OUT, initial=GPIO.HIGH)

def accState(roomNumber, accNumber):
	accesory = rooms[roomNumber]['Accesories'][accNumber]
	if accesory['Type'] == 'Pin':
		if GPIO.input(accesory['Value']) is 1:
			return 'containerOff'
		else:
			return 'containerOn'
	else:
		#get the state of other accesories in other rooms
		#not implemented yet
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
	i = 0
	for room in rooms:
		passer = passer + "<p class='roomtitle'>%s</p>" % (room['Name'])
		j = 0
		for accesory in room['Accesories']:
			buttonHtmlName = accesory['Name'].replace(" ", "<br>")
			passer = passer + "<span id='button%d%d'><button class='%s' onclick='toggle(%d,%d)'>%s</button></span>" % (i, j, accState(i,j), i, j, buttonHtmlName)
			j = j+1
		i = i+1
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
	i = 0
	for room in rooms:
		passer = passer + "<p class='roomtitle'>%s</p>" % (room['Name'])
		j = 0
		for accesory in room['Accesories']:
			buttonHtmlName = accesory['Name'].replace(" ", "<br>")
			passer = passer + "<span id='button%d%d'><button class='%s' onclick='toggle(%d,%d)'>%s</button></span>" % (i, j, accState(i,j), i, j, buttonHtmlName)
			j = j+1
		i = i+1
	return passer

@app.route("/statelist/")
def buttonStates():
	accState=[]
	i = 0
	for room in rooms:
		j = 0
		accState.append([])
		for accesory in room['Accesories']:
			accState[i].append(1 - GPIO.input(accesory['Value']))
			j = j+1
		i = i+1
	return json.dumps(accState)

@app.route("/setstate/<int:roomNumber>/<int:accNumber>/<int:state>/")
def setstate(roomNumber, accNumber, state):
	accesory = rooms[roomNumber]['Accesories'][accNumber]
	if accesory['Type'] == 'Pin':
		GPIO.output(accesory['Value'], 1 - state)
		#subprocess.call(['./echo.sh'], shell=True)
	else:
		#action for other rooms
		subprocess.call([accesory['Value']], shell=True)
	return "0"

							   
@app.route("/button/<int:roomNumber>/<int:accNumber>/")
@crossdomain(origin='*')
def toggle(roomNumber, accNumber):
	accesory = rooms[roomNumber]['Accesories'][accNumber]
	if accesory['Type'] == 'Pin':
		state= 1 - GPIO.input(accesory['Value'])
		GPIO.output(accesory['Value'], state)
		#subprocess.call(['./echo.sh'], shell=True)
	else:
		#action for other rooms
		subprocess.call([accesory['Value']], shell=True)
	#print(roomNumber, accNumber)
	buttonHtmlName = accesory['Name'].replace(" ", "<br>")
	passer="<button class='%s' onclick='toggle(%d,%d)'>%s</button>" % (accState(roomNumber,accNumber), roomNumber, accNumber, buttonHtmlName)
	return passer


if __name__ == "__main__":
	if secure:
		cerPath=os.path.join(sys.path[0], "WebGPIO.cer")
		keyPath=os.path.join(sys.path[0], "WebGPIO.key")
		app.run(host='0.0.0.0', port=8000, debug=True, ssl_context=(cerPath, keyPath))
	else:
		app.run(host='0.0.0.0', port=8000, debug=True)

