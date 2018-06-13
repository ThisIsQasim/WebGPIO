import subprocess, datetime, time, json
from flask import Flask, render_template, redirect, Markup
from lib.cors import crossdomain
from lib.setup import rooms, settings
from lib.GPIOSetup import GPIO

app = Flask(__name__)


def getState(roomNumber, accNumber):
	accesory = rooms[roomNumber]['Accesories'][accNumber]
	if accesory['Type'] == 'Pin':
		if GPIO.input(accesory['Value']) is settings['ActiveValue']:
			return 1
		else:
			return 0
	else:
		#get the state of other accesories in other rooms
		#not properly implemented yet
		try:
			timeout = "timeout "+str(accesory['Timeout'])+" "
		except Exception:
			timeout = "timeout 0.2 "
		returnCode = subprocess.call([timeout + accesory['Value']], shell=True)
		if returnCode == 0:
			return 1
		return 0

def updateStates(rooms):
	for i, room in enumerate(rooms):
		for j, accesory in enumerate(room['Accesories']):
			rooms[i]['Accesories'][j]['State'] = getState(i,j)
	return rooms

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)


@app.route("/")
def main():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %I:%M %p")
	templateData = {
		'title' : 'WebGPIO',
		'time': timeString,
		'rooms' : updateStates(rooms),
		'refresh_rate' : settings['RefreshRate']*1000
	}
	return render_template('main.html', **templateData)

@app.route("/grid/")
@crossdomain(origin='*')
def grid():
	templateData = {
		'title' : 'WebGPIO',
		'rooms' : updateStates(rooms)
	}
	return render_template('grid.html', **templateData)

@app.route("/button/<int:roomNumber>/<int:accNumber>/")
@crossdomain(origin='*')
def toggle(roomNumber, accNumber):
	accesory = rooms[roomNumber]['Accesories'][accNumber]
	if accesory['Type'] == 'Pin':
		state= 1 - GPIO.input(accesory['Value'])
		GPIO.output(accesory['Value'], state)
	templateData = {
		'title' : 'WebGPIO',
		'state' : getState(roomNumber, accNumber),
		'roomNumber' : roomNumber,
		'accNumber' : accNumber,
		'name' : accesory['Name']
	}
	return render_template('button.html', **templateData)


if __name__ == "__main__":
	if settings['SSL']['Enabled']:
		app.run(host = settings['Host'], 
				port = settings['Port'], 
				threaded = settings['Threaded'], 
				debug = settings['Debug'], 
				ssl_context = (settings['cerPath'], settings['keyPath']))
	else:
		app.run(host = settings['Host'], 
				port = settings['Port'], 
				threaded = settings['Threaded'], 
				debug = settings['Debug'])