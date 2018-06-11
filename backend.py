from datetime import timedelta
from functools import update_wrapper
from flask import Flask, render_template, redirect, Markup, make_response, request, current_app
import RPi.GPIO as GPIO
import subprocess, os, sys, datetime, time, json, yaml

configPath = os.path.join(sys.path[0], "config.yml")
with open(configPath, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

rooms = cfg['Rooms']
settings = cfg['Settings']
app = Flask(__name__)

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
		try:
			timeout = "timeout "+str(accesory['Timeout'])+" "
		except Exception:
			timeout = "timeout 0.2 "
		returnCode = subprocess.call([timeout + accesory['Value']], shell=True)
		if returnCode == 0:
			return 'containerOn'
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

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.route("/")
def main():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %I:%M %p")
	for i, room in enumerate(rooms):
		for j, accesory in enumerate(room['Accesories']):
			rooms[i]['Accesories'][j]['accState'] = accState(i,j)
	templateData = {
		'title' : 'WebGPIO',
		'time': timeString,
		'rooms' : rooms
	}
	return render_template('main.html', **templateData)

@app.route("/grid/")
@crossdomain(origin='*')
def grid():
	for i, room in enumerate(rooms):
		for j, accesory in enumerate(room['Accesories']):
			rooms[i]['Accesories'][j]['accState'] = accState(i,j)
	templateData = {
		'title' : 'WebGPIO',
		'rooms' : rooms
	}
	return render_template('grid.html', **templateData)

@app.route("/button/<int:roomNumber>/<int:accNumber>/")
@crossdomain(origin='*')
def toggle(roomNumber, accNumber):
	accesory = rooms[roomNumber]['Accesories'][accNumber]
	if accesory['Type'] == 'Pin':
		state= 1 - GPIO.input(accesory['Value'])
		GPIO.output(accesory['Value'], state)
	# else:
	# 	#action for other rooms
	# 	try:
	# 		timeout = "timeout "+str(accesory['Timeout'])+" "
	# 	except Exception:
	# 		timeout = "timeout 0.2 "
	# 	subprocess.call([timeout + accesory['Value']], shell=True)
	templateData = {
		'title' : 'WebGPIO',
		'accState' : accState(roomNumber, accNumber),
		'roomNumber' : roomNumber,
		'accNumber' : accNumber,
		'name' : accesory['Name']
	}
	return render_template('button.html', **templateData)

#Deprecated routes	
@app.route("/statelist/")
def buttonStates():
	accState=[]
	for i, room in enumerate(rooms):
		accState.append([])
		for j, accesory in enumerate(room['Accesories']):
			if accesory['Type'] == 'Pin':
				accState[i].append(1 - GPIO.input(accesory['Value']))
			else:
				accState[i].append(2)
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


if __name__ == "__main__":
	if settings['SSL']['Enabled']:
		if settings['SSL']['Path'] == 'default':
			cerPath=os.path.join(sys.path[0], settings['SSL']['Certificate'])
			keyPath=os.path.join(sys.path[0],  settings['SSL']['Key'])
		else:
			cerPath=settings['SSL']['Path'] + settings['SSL']['Certificate']
			keyPath=settings['SSL']['Path'] + settings['SSL']['Key']	
		app.run(host='0.0.0.0', port=8000, threaded=True, debug=True, ssl_context=(cerPath, keyPath))
	else:
		app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)