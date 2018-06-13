import datetime, json
from flask import Flask, render_template, redirect, Markup
from lib.cors import crossdomain
from lib.setup import rooms, settings
from lib.GPIOSetup import GPIO
from lib.accesory import accesoryObject
app = Flask(__name__)


def updateStates(rooms):
	for i, room in enumerate(rooms):
		for j, accesory in enumerate(room['Accesories']):
			current_accesory = accesoryObject(accesory)
			rooms[i]['Accesories'][j]['State'] = current_accesory.getState()
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
def button(roomNumber, accNumber):
	current_accesory = accesoryObject(rooms[roomNumber]['Accesories'][accNumber])
	current_accesory.executeAction()
	templateData = {
		'title' : 'WebGPIO',
		'state' : current_accesory.getState(),
		'roomNumber' : roomNumber,
		'accNumber' : accNumber,
		'name' : current_accesory.name
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